from flask import Flask, render_template, request
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

app = Flask(__name__)

model = joblib.load("aqi_model.pkl")

FEATURES = ["PM2.5", "PM10", "O3", "NO2", "SO2", "CO"]


def get_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"


def load_aqi_data():

    df = pd.read_excel("airpollution.xlsx")

    df["AQI"] = pd.to_numeric(df["AQI"], errors="coerce")

    df = df[
        (df["AQI"] >= 0) &
        (df["AQI"] <= 500)
    ].copy()

    for col in FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    df = df.dropna(
        subset=["Latitude", "Longitude", "AQI"]
    )

    india_df = df[
        (df["Latitude"] >= 6) &
        (df["Latitude"] <= 38) &
        (df["Longitude"] >= 68) &
        (df["Longitude"] <= 98)
    ].copy()

    cluster_features = ["Latitude", "Longitude", "AQI"]

    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(
        india_df[cluster_features]
    )

    kmeans = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    india_df["Cluster"] = kmeans.fit_predict(
        scaled_data
    )

    cluster_means = india_df.groupby(
        "Cluster"
    )["AQI"].mean()

    high_cluster = cluster_means.idxmax()
    low_cluster = cluster_means.idxmin()

    labels = {}

    for cluster in cluster_means.index:

        if cluster == high_cluster:
            labels[cluster] = "High Pollution"

        elif cluster == low_cluster:
            labels[cluster] = "Low Pollution"

        else:
            labels[cluster] = "Moderate Pollution"

    india_df["Cluster_Label"] = india_df[
        "Cluster"
    ].map(labels)

    return india_df


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    result = None
    category = None

    if request.method == "POST":

        pm25 = float(request.form["pm25"])
        pm10 = float(request.form["pm10"])
        o3 = float(request.form["o3"])
        no2 = float(request.form["no2"])
        so2 = float(request.form["so2"])
        co = float(request.form["co"])

        data = pd.DataFrame(
            [[pm25, pm10, o3, no2, so2, co]],
            columns=FEATURES
        )

        result = round(
            float(model.predict(data)[0]),
            2
        )

        category = get_category(result)

    return render_template(
        "prediction.html",
        prediction=result,
        category=category
    )


@app.route("/map")
def pollution_map():

    df = load_aqi_data()

    locations = []

    for _, row in df.iterrows():

        locations.append({
            "city": str(row["City"]),
            "aqi": round(float(row["AQI"]), 2),
            "lat": float(row["Latitude"]),
            "lng": float(row["Longitude"]),
            "cluster": str(row["Cluster_Label"])
        })

    cluster_summary = (
        df.groupby("Cluster_Label")["AQI"]
        .agg(["mean", "count"])
        .reset_index()
    )

    summary = {}

    for _, row in cluster_summary.iterrows():

        summary[row["Cluster_Label"]] = {
            "avg_aqi": round(float(row["mean"]), 2),
            "count": int(row["count"])
        }

    return render_template(
        "map.html",
        locations=locations,
        summary=summary
    )


@app.route("/pollutants")
def pollutants():
    return render_template("pollutants.html")


@app.route("/clustering")
def clustering():
    return render_template("clustering.html")


@app.route("/dataset")
def dataset():
    return render_template("dataset.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)