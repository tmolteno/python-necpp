# Note: explicit zeroes are blanks. All other values should be specified symbolically.

# Currently these contain only the subset of cards that I needed

class context_clean(object):
    def __init__(self, context):
        self.context = context

    def remove_all_loads(self):
        ld_short_all_loads = -1
        self.context.ld_card(ld_short_all_loads, 0, 0, 0, 0, 0, 0)

    def set_wire_conductivity(self, conductivity, wire_tag=None):
        """ The conductivity is specified in mhos/meter. Currently all segments of a wire are set. If wire_tag is None, all wire_tags are set (i.e., a tag of 0 is used). """
        if wire_tag is None:
            wire_tag = 0
        self.context.ld_card(5, wire_tag, 0, 0, conductivity, 0, 0)

    def set_all_wires_conductivity(self, conductivity):
        self.set_wire_conductivity(conductivity)

    # TODO: multiplicative
    def set_frequencies_linear(self, start_frequency, stop_frequency, count=None, step_size=None):
        """ If start_frequency does not equal stop_frequency, either count or step should be specified. The other parameter will be automatically deduced """

        if start_frequency == stop_frequency:
            step_size = 0
            count = 1
        else:
            # TODO: add some asserts
            if count is not None:
                step_size = (stop_frequency - start_frequency) / count
            else:
                count = (stop_frequency - start_frequency) / step_size

        # TODO, what if we don't have nice divisibility here
        count = int(count)

        ifrq_linear_step = 0
        self.context.fr_card(ifrq_linear_step, count, start_frequency, step_size)

    def set_frequency(self, frequency):
        self.set_frequencies_linear(frequency, frequency)

    def clear_ground(self):
        gn_nullify_ground = -1
        self.context.gn_card(gn_nullify_ground, 0, 0, 0, 0, 0, 0, 0)

    # TODO: gn card is iffy, check!
    def set_finite_ground(self, ground_dielectric, ground_conductivity):
        gn_finite_ground = 0
        no_ground_screen = 0

        self.context.gn_card(gn_finite_ground, no_ground_screen, ground_dielectric, ground_conductivity, 0, 0, 0, 0)

    # TODO: i1 = 5 is also a voltage excitation
    def voltage_excitation(self, wire_tag, segment_nr, voltage):
        ex_voltage_excitation = 0
        no_action = 0 # TODO configurable
        option_i3i4 = 10*no_action + no_action

        self.context.ex_card(ex_voltage_excitation, wire_tag, segment_nr, option_i3i4, voltage.real, voltage.imag, 0, 0, 0, 0)

    def get_geometry(self):
        #return geometry_clean(self.context.get_geometry()) # TODO
        return self.context.get_geometry()

    def set_extended_thin_wire_kernel(self, enable):
        if enable:
            self.context.set_extended_thin_wire_kernel(1)
        else:
            self.context.set_extended_thin_wire_kernel(0)

    # Some simple wrappers for context...
    # TODO: this should be simpler, can't this be auto-generated, or implicitly defined? The best solution is of course to do this in the C++ code,
    # and then the wrappers are immediately correct and nice

    def geometry_complete(self, *args):
        return self.context.geometry_complete(*args)
    def xq_card(self, *args):
        return self.context.xq_card(*args)
    def get_input_parameters(self, *args):
        return self.context.get_input_parameters(*args)

class geometry_clean(object):
    def __init__(self, geometry):
        self.geometry = geometry

    def wire(self, tag_id, nr_segments, src, dst, radius, length_ratio=1.0, radius_ratio=1.0):
        """ radius is in meter. length_ratio can be set to have non-uniform segment lengths, radius_ratio can be used for tapered wires """
        self.geometry.wire(tag_id, nr_segments, src[0], src[1], src[2], dst[0], dst[1], dst[2], radius, length_ratio, radius_ratio)
