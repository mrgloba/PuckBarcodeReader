import uuid

from dls_barcode.geometry import Geometry
from .slot import Slot, EMPTY_SLOT_SYMBOL, NOT_FOUND_SLOT_SYMBOL


class Plate:
    """ Represents a sample holder plate.
    """
    def __init__(self, geometry_name, num_slots=-1):
        self.id = str(uuid.uuid1())

        if num_slots == -1:
            self.num_slots = Geometry.get_num_slots(geometry_name)
        else:
            self.num_slots = num_slots

        self.type = geometry_name
        self._geometry = None

        # Initialize slots
        self._slots = [Slot(i) for i in range(1, self.num_slots+1)]

    #########################
    # ACCESSOR FUNCTIONS
    #########################
    def slot(self, i):
        """ Get the numbered slot on this sample plate."""
        return self._slots[i - 1]

    def slots(self):
        return self._slots[:]

    def barcodes(self):
        """ Returns a list of barcode strings. Empty slots are represented by the empty string.
        """
        return [slot.barcode_data() for slot in self._slots]

    def geometry(self):
        return self._geometry

    def set_geometry(self, geometry):
        self._geometry = geometry
        for slot in self._slots:
            bounds = geometry.slot_bounds(slot.number())
            slot.set_bounds(bounds)

    def invalid_slots(self):
        return [s for s in self._slots if s.state() != Slot.VALID]

    #########################
    # STATUS FUNCTIONS
    #########################
    def num_empty_slots(self):
        return len([slot for slot in self._slots if slot.state() == Slot.EMPTY])

    def num_valid_barcodes(self):
        return len([slot for slot in self._slots if slot.state() == Slot.VALID])

    def num_unread_barcodes(self):
        return self.num_slots - self.num_valid_barcodes() - self.num_empty_slots()

    def is_full_valid(self):
        return (self.num_valid_barcodes() + self.num_empty_slots()) == self.num_slots

    def contains_barcode(self, barcode):
        """ Returns true if the plate contains a slot with the specified barcode value. """
        if barcode == EMPTY_SLOT_SYMBOL or barcode == NOT_FOUND_SLOT_SYMBOL:
            return False

        for b in self.barcodes():
            if b == barcode:
                return True

        return False

    def has_slots_in_common(self, plate_b):
        """ Returns true if the specified plate has any slots with valid barcodes in
        common with this plate.
        """
        plate_a = self
        if plate_a.type != plate_b.type:
            return False

        for i, slot_a in enumerate(plate_a._slots):
            slot_b = plate_b.slot(i+1)
            if slot_a.state() == Slot.VALID:
                if slot_a.barcode_data() == slot_b.barcode_data():
                    return True

        return False

    #########################
    # DRAWING FUNCTIONS
    #########################
    def draw_barcodes(self, img, color):
        for slot in self._slots:
            if slot.state() == slot.VALID:
                slot.barcode().draw(img, color)

    def draw_plate(self, img, color):
        self._geometry.draw_plate(img, color)

    def draw_pins(self, img, options):
        for i, slot in enumerate(self._slots):
            state = slot.state()
            if state == Slot.VALID:
                color = options.col_ok()
            elif state == Slot.EMPTY:
                color = options.col_empty()
            else:
                color = options.col_bad()
            self._geometry.draw_pin_highlight(img, color, i + 1)

    def crop_image(self, img):
        self._geometry.crop_image(img)
