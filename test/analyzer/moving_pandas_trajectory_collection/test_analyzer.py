import os.path
import tempfile
from unittest import TestCase
from src.analyzer.moving_pandas_trajectory_collection.analyzer import MovingPandasAnalyzer
from test.config.definitions import ROOT_DIR
from test.config.fixtures import gzip_copy


class TestMovingPandasAnalyzer(TestCase):

    def setUp(self) -> None:
        self.sut = MovingPandasAnalyzer()
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_it_should_handle_empty_input(self):
        # execute
        actual = self.sut.analyze(path=self.__test_file("empty.pickle"))

        # verify
        self.assertEqual(actual[0]['n'], ["empty-result"])

    def test_it_should_analyze_input1_LatLon(self):
        # execute
        actual = self.sut.analyze(path=self.__test_file("input1_LatLon.pickle"))

        # verify
        self.assertEqual(actual[0]['positions_total_number'], 3243)
        self.assertEqual(actual[1]['timestamps_range'], ['2021-07-01 06:40:00', '2022-03-15 14:13:00'])
        self.assertEqual(actual[2]['animals_total_number'], 1)
        self.assertEqual(actual[3]['animal_names'], ['Goat-8810'])
        self.assertEqual(actual[4]['taxa'], ['Capra hircus'])
        self.assertEqual(actual[5]['sensor_types'], ['GPS'])
        self.assertEqual(actual[6]['positions_bounding_box'], {'x_min': 14.9216333333333, 'y_min': 37.8303666666667, 'x_max': 14.9606333333333, 'y_max': 37.8717833333333})
        self.assertEqual(actual[7]['projection'], 'EPSG:4326')
        self.assertEqual(actual[8]['tracks_total_number'], 1)
        self.assertEqual(actual[9]['track_names'], ['Goat.8810..deploy_id.1600804509.'])
        self.assertEqual(actual[10]['number_positions_by_track'], {'Goat.8810..deploy_id.1600804509.': 3243})
        self.assertEqual(actual[11]['data_attributes'], ['sensor_type_id', 'comments', 'data_decoding_software', 'gps_horizontal_accuracy_estimate', 'gps_speed_accuracy_estimate', 'gps_time_to_fix', 'ground_speed', 'heading', 'height_above_ellipsoid', 'icarus_ecef_vx', 'icarus_ecef_vy', 'icarus_ecef_vz', 'icarus_ecef_x', 'icarus_ecef_y', 'icarus_ecef_z', 'icarus_reset_counter', 'icarus_timestamp_accuracy', 'icarus_timestamp_source', 'icarus_uplink_counter', 'import_marked_outlier', 'location_error_text', 'manually_marked_outlier', 'mortality_status', 'sequence_number', 'sigfox_rssi', 'tag_voltage', 'timestamp', 'transmission_protocol', 'transmission_timestamp', 'event_id', 'visible', 'individual_name_deployment_id', 'deployment_id', 'tag_id', 'individual_id', 'animal_life_stage', 'animal_reproductive_condition', 'attachment_type', 'deploy_off_timestamp', 'deploy_on_person', 'deploy_on_timestamp', 'sensor_type_ids', 'capture_location', 'deploy_on_location', 'deploy_off_location', 'nick_name', 'ring_id', 'sex', 'taxon_canonical_name', 'individual_number_of_deployments', 'mortality_location', 'tag_local_identifier', 'tag_number_of_deployments', 'study_id', 'acknowledgements', 'citation', 'grants_used', 'has_quota', 'i_am_owner', 'is_test', 'license_terms', 'license_type', 'name', 'study_number_of_deployments', 'number_of_individuals', 'number_of_tags', 'principal_investigator_name', 'study_objective', 'study_type', 'suspend_license_terms', 'i_can_see_data', 'there_are_data_which_i_cannot_see', 'i_have_download_access', 'i_am_collaborator', 'study_permission', 'timestamp_first_deployed_location', 'timestamp_last_deployed_location', 'number_of_deployed_locations', 'taxon_ids', 'contact_person_name', 'main_location', 'individual_local_identifier', 'timestamp_tz', 'geometry'])
        self.assertEqual(actual[12]['n'], ['non-empty-result'])

    def test_it_should_analyze_input4_LatLon(self):
        # execute
        actual = self.sut.analyze(path=self.__test_file("input4_LatLon.pickle"))

        # verify
        self.assertEqual(actual[0]['positions_total_number'], 7770)
        self.assertEqual(actual[1]['timestamps_range'], ['2013-08-07 18:27:02', '2015-02-19 13:42:27'])
        self.assertEqual(actual[2]['animals_total_number'], 'total number of animals is not available')
        self.assertEqual(actual[3]['animal_names'], 'no appropriate animal names available')
        self.assertEqual(actual[4]['taxa'], 'no appropriate taxa names available')
        self.assertEqual(actual[5]['sensor_types'], ['GPS'])
        self.assertEqual(actual[6]['positions_bounding_box'], {'x_min': 3.7317, 'y_min': 49.417633, 'x_max': 53.619633, 'y_max': 69.156667})
        self.assertEqual(actual[7]['projection'], 'EPSG:4326')
        self.assertEqual(actual[8]['tracks_total_number'], 3)
        self.assertEqual(actual[9]['track_names'], ['X742..deploy_id.56853924.', 'X746..deploy_id.20813885.', 'X749..deploy_id.20813892.'])
        self.assertEqual(actual[10]['number_positions_by_track'], {'X742..deploy_id.56853924.': 3265, 'X746..deploy_id.20813885.': 3010, 'X749..deploy_id.20813892.': 1495})
        self.assertEqual(actual[11]['data_attributes'], ['sensor_type_id', 'barometric_pressure', 'data_decoding_software', 'eobs_activity', 'eobs_activity_samples', 'eobs_battery_voltage', 'eobs_fix_battery_voltage', 'eobs_horizontal_accuracy_estimate', 'eobs_key_bin_checksum', 'eobs_speed_accuracy_estimate', 'eobs_start_timestamp', 'eobs_status', 'eobs_temperature', 'eobs_type_of_fix', 'eobs_used_time_to_get_fix', 'gps_dop', 'gps_satellite_count', 'ground_speed', 'gt_tx_count', 'heading', 'height_above_ellipsoid', 'height_raw', 'import_marked_outlier', 'manually_marked_outlier', 'tag_voltage', 'timestamp', 'event_id', 'visible', 'individual_name_deployment_id', 'timestamp_tz', 'geometry'])
        self.assertEqual(actual[12]['n'], ['non-empty-result'])

    def test_it_should_analyze_a_gzip_compressed_input4_LatLon(self):
        # prepare: an App on Python SDK v3 writes gzip-compressed output, under a file name that
        # carries no extension
        compressed = gzip_copy(
            self.__test_file("input4_LatLon.pickle"),
            os.path.join(self.tmp.name, "output_file")
        )

        # execute
        actual = self.sut.analyze(path=compressed)

        # verify: the compression makes no difference to the statistics
        self.assertEqual(actual[0]['positions_total_number'], 7770)
        self.assertEqual(actual[1]['timestamps_range'], ['2013-08-07 18:27:02', '2015-02-19 13:42:27'])
        self.assertEqual(actual[8]['tracks_total_number'], 3)
        self.assertEqual(actual[10]['number_positions_by_track'], {'X742..deploy_id.56853924.': 3265, 'X746..deploy_id.20813885.': 3010, 'X749..deploy_id.20813892.': 1495})
        self.assertEqual(actual[12]['n'], ['non-empty-result'])

    def __test_file(self, file_name) -> str:
        return os.path.join(ROOT_DIR, 'test', 'resources', 'moving_pandas_trajectory_collection', file_name)
