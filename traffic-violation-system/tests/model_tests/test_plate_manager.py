import unittest
import numpy as np
import cv2
from app.services.number_plate.plate_manager import plate_manager

class TestPlateManager(unittest.TestCase):
    def setUp(self):
        plate_manager.plates.clear()
        plate_manager.track_to_plate.clear()
        plate_manager.next_plate_id = 1
        plate_manager.total_plates_detected = 0

    def test_plate_containment_and_registration(self):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Draw some text/noise on frame to avoid blur check rejection
        cv2.putText(frame, "IND MH12DE1432 PROOF", (110, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # 1. Reject plate if outside vehicle box
        vehicle_box = [50, 50, 400, 400]
        plate_box_outside = [10, 10, 80, 30]
        plate_manager.register_plate(frame, vehicle_box, plate_box_outside, 0.95, 17, "car", 522)
        
        self.assertEqual(len(plate_manager.get_all_plates()), 0)

        # 2. Register valid plate inside vehicle box
        plate_box_inside = [100, 200, 250, 240]
        plate_manager.register_plate(frame, vehicle_box, plate_box_inside, 0.95, 17, "car", 522)
        
        all_plates = plate_manager.get_all_plates()
        self.assertEqual(len(all_plates), 1)
        self.assertEqual(all_plates[0]["track_id"], 17)
        self.assertEqual(all_plates[0]["confidence"], 0.95)

        # 3. Update plate if higher confidence comes in
        plate_manager.register_plate(frame, vehicle_box, plate_box_inside, 0.98, 17, "car", 523)
        
        all_plates = plate_manager.get_all_plates()
        self.assertEqual(len(all_plates), 1)
        self.assertEqual(all_plates[0]["confidence"], 0.98)
        self.assertEqual(all_plates[0]["frame"], 523)

if __name__ == "__main__":
    unittest.main()
