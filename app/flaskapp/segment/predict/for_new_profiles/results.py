import numpy as np
import joblib, os, sys

fileDir = os.path.dirname(__file__)
#fileDir = os.path.join(fileDir,'..')
modelsPath = os.path.abspath(os.path.join(fileDir, 'models'))
#logPath = os.path.abspath(os.path.join(fileDir, 'logs'))
sys.path.insert(0, modelsPath)
#sys.path.insert(0,logPath)

scaler_file = os.path.join(modelsPath, 'StdScaler.pkl')
predictor_file = os.path.join(modelsPath, 'kmeans_fls.pkl')


def predictSegment(min_starting_rate, max_starting_rate, min_hourly_rate, max_hourly_rate):
    min_starting_rate = int(min_starting_rate)
    max_starting_rate = int(max_starting_rate)
    min_hourly_rate = int(min_hourly_rate)
    max_hourly_rate = int(max_hourly_rate)

    entry = np.array([0.0, min_starting_rate, max_starting_rate, min_hourly_rate, max_hourly_rate, 1.0]).reshape(1, -1)

    scaler = joblib.load(scaler_file)

    entry_scaled = scaler.transform(entry)

    predictor = joblib.load(predictor_file)

    profile_cluster_id = (predictor.predict(entry_scaled))[0]

    return int(profile_cluster_id)


    