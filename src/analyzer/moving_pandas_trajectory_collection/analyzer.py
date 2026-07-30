from geopandas import GeoDataFrame

from src.analyzer.base_analyzer import BaseAnalyzer
from src.moveapps_pickle import MoveAppsPickle

import geopandas as gpd
import movingpandas as mpd
import logging


class MovingPandasAnalyzer(BaseAnalyzer):

    def analyze(self, path: str) -> list:
        movingpandas = self.__read(path=path)
        geopandas = self.__convert(movingpandas=movingpandas)
        if geopandas is not None:
            return self.__inspect(data=geopandas, movingpandas=movingpandas)
        else:
            return [{
                # The field `n` is special and expects its value of type array.
                # MoveApps should simply that in the future.
                "n": ["empty-result"]
            }]

    def __read(self, path: str) -> mpd.TrajectoryCollection:
        movingpandas = MoveAppsPickle.read(path=path)
        logging.info(f'read movingpandas: {movingpandas}')
        return movingpandas

    def __convert(self, movingpandas: mpd.TrajectoryCollection) -> GeoDataFrame | None:
        if len(movingpandas.trajectories) > 0:
            # Converting to geopandas is only possible if at least 1 trajectory is present
            geopandas = movingpandas.to_point_gdf()
            print(f'From {type(movingpandas)} to {type(geopandas)}')
            logging.info(geopandas.info())
            logging.info(geopandas.head())
            return geopandas
        else:
            return None

    def __inspect(self, data: gpd.GeoDataFrame, movingpandas: mpd.TrajectoryCollection) -> list:

        # The field `n` is special and expects its value of type array.
        # MoveApps should simply that in the future.
        n = ["non-empty-result"]

        positions_total_number = len(data)
        
        timestamps_range = [str(data.index.min()),str(data.index.max())]

        traj_id_col = movingpandas.get_traj_id_col()
        track_names = data[traj_id_col].unique().tolist()
        tracks_total_number = len(track_names)

        geom_col = movingpandas.get_geom_col()
        number_positions_by_track = dict(data.dissolve(by=traj_id_col, aggfunc={traj_id_col: "count"}).drop(geom_col, axis=1).rename(columns={traj_id_col: "count"}).reset_index().values)

        projection = movingpandas.get_crs()

        #positions_bounding_box = data.total_bounds.tolist()
        positions_bounding_box = data.total_bounds
        positions_bounding_box = dict({"x_min": positions_bounding_box[0], "y_min": positions_bounding_box[1], "x_max": positions_bounding_box[2], "y_max": positions_bounding_box[3]})

        track_attributes = data.columns.tolist()

        if 'individual-local-identifier' in data:
            animal_names = data['individual.local.identifier'].unique().tolist()
            animals_total_number=len(animal_names)
        elif 'individual_local_identifier' in data:
            animal_names = data['individual_local_identifier'].unique().tolist()
            animals_total_number=len(animal_names)
        else:
            animal_names = "no appropriate animal names available"
            animals_total_number = "total number of animals is not available"

        sensor_ids = [397, 653, 673, 82798, 2365682, 2365683, 3886361, 7842954, 9301403, 77740391, 77740402, 819073350, 914097241, 1239574236, 1297673380, 2206221896, 2299894820, 2645090675]
        sensor_names = ["Bird Ring", "GPS", "Radio Transmitter", "Argos Doppler Shift", "Natural Mark", "Acceleration", "Solar Geolocator", "Accessory Measurements", "Solar Geolocator Raw", "Barometer", "Magnetometer", "Orientation", "Solar Geolocator Twilight", "Acoustic Telemetry", "Gyroscope", "Heart Rate", "Sigfox Geolocation", "Proximity"]
        sensor_info = {sensor_ids[i]: sensor_names[i] for i in range(len(sensor_ids))}
        
        if "sensor.type" in data:
            sensor_types = data["sensor-type"].unique().tolist()
        elif "sensor_type" in data:
            sensor_types = data["sensor_type"].unique().tolist()
        elif "sensor-type-id" in data:
            sensor_types = [sensor_info[i] for i in data["sensor-type-id"].unique().tolist()]
        elif "sensor_type_id" in data:
            sensor_types = [sensor_info[i] for i in data["sensor_type_id"].unique().tolist()]
        else:
            sensor_types = "no sensor type data found"

        if 'individual-taxon-canonical-name' in data:
            taxa = data['individual-taxon-canonical-name'].unique().tolist()
        elif 'individual_taxon_canonical_name' in data:
            taxa = data['individual_taxon_canonical_name'].unique().tolist()
        elif 'taxon-canonical-name' in data:
            taxa = data['taxon-canonical-name'].unique().tolist()
        elif 'taxon_canonical_name' in data:
            taxa = data['taxon_canonical_name'].unique().tolist()
        else:
            taxa = "no appropriate taxa names available"

        return [
            {"positions_total_number": positions_total_number},  # 0
            {"timestamps_range": timestamps_range},
            {"animals_total_number": animals_total_number},  # 2
            {"animal_names": animal_names},
            {"taxa": taxa},  # 4
            {"sensor_types": sensor_types},
            {"positions_bounding_box": positions_bounding_box},  # 6
            {"projection": projection},
            {"tracks_total_number": tracks_total_number},  # 8
            {"track_names": track_names},
            {"number_positions_by_track": number_positions_by_track},  # 10
            {"data_attributes": track_attributes},
            {"n": n},  # 12
        ]

