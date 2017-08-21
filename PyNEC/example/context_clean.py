# Note: explicit zeroes are blanks. All other values should be specified symbolically.

# Currently these contain only the subset of cards that I needed

class Range(object):
    def __init__(self, start, stop, count=None, delta=None):
        self.start = start
        self.stop = stop
        if count is not None:
            self.count = count
            self.delta = (stop - start) / count
        else:
            self.count = (stop_ - start) / delta
            self.delta = delta

# Setting do_debug to True will dump all the cards generated with context_clean, so you can verify the output more easily in a text editor (and debug that file manually)
do_debug = False

def debug(card, *args):
    if do_debug:
        stringified = " , ".join([str(a) for a in args])
        print "%s %s" % (card, stringified)

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

        debug("LD", 5, wire_tag, 0, 0, conductivity, 0, 0)
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
        debug("FR", ifrq_linear_step, count, start_frequency, step_size, 0, 0, 0)
        self.context.fr_card(ifrq_linear_step, count, start_frequency, step_size)

    def set_frequency(self, frequency):
        self.set_frequencies_linear(frequency, frequency)

    def clear_ground(self):
        gn_nullify_ground = -1
        self.context.gn_card(gn_nullify_ground, 0, 0, 0, 0, 0, 0, 0)

    # TODO: I could probably make a ground class, would probably be cleaner to group some of the options and different functions there (like combining ground screen etc)

    # TODO: gn card is iffy, check!
    def set_finite_ground(self, ground_dielectric, ground_conductivity):
        gn_finite_ground = 0
        no_ground_screen = 0

        self.context.gn_card(gn_finite_ground, no_ground_screen, ground_dielectric, ground_conductivity, 0, 0, 0, 0)

    def set_perfect_ground(self):
        gn_perfectly_conducting = 1
        no_ground_screen = 0

        debug("GN", gn_perfectly_conducting, no_ground_screen, 0, 0, 0, 0, 0, 0)
        self.context.gn_card(gn_perfectly_conducting, no_ground_screen, 0, 0, 0, 0, 0, 0)


    # TODO: i1 = 5 is also a voltage excitation
    def voltage_excitation(self, wire_tag, segment_nr, voltage):
        ex_voltage_excitation = 0
        no_action = 0 # TODO configurable
        option_i3i4 = 10*no_action + no_action

        debug("EX", ex_voltage_excitation, wire_tag, segment_nr, option_i3i4, voltage.real, voltage.imag, 0, 0, 0, 0)
        self.context.ex_card(ex_voltage_excitation, wire_tag, segment_nr, option_i3i4, voltage.real, voltage.imag, 0, 0, 0, 0)

    def get_geometry(self):
        #return geometry_clean(self.context.get_geometry()) # TODO
        return self.context.get_geometry()

    def set_extended_thin_wire_kernel(self, enable):
        if enable:
            debug ("EK", 0)
            self.context.set_extended_thin_wire_kernel(1)
        else:
            debug ("EK", -1)
            self.context.set_extended_thin_wire_kernel(0)

    def geometry_complete(self, ground_plane, current_expansion=True):
        no_ground_plane = 0
        ground_plane_current_expansion = 1
        ground_plane_no_current_expansion = -1
        if not ground_plane:
            debug("GE", no_ground_plane)
            self.context.geometry_complete(no_ground_plane)
        else:
            if current_expansion:
                debug("GE", ground_plane_current_expansion)
                self.context.geometry_complete(ground_plane_current_expansion)
            else:
                debug("GE", ground_plane_no_current_expansion)
                self.context.geometry_complete(ground_plane_no_current_expansion)

    output_major_minor = 0
    output_vertical_horizontal = 1

    normalization_none = 0
    normalization_major = 1
    normalization_minor = 2
    normalization_vertical = 3
    normalization_horizontal = 4
    normalization_totalgain = 5

    power_gain = 0
    directive_gain = 1

    average_none = 0
    average_gain = 1
    average_todo = 2

    # TODO: this should be different for surface_wave_mode (1), because then thetas = z
    def radiation_pattern(self, thetas, phis, output_mode=output_vertical_horizontal, normalization=normalization_none, gain=power_gain, average=average_todo):
        """ thetas and phis should be Range(-like) objects """
        normal_mode = 0 # TODO other modes

        # the rp_card already has XNDA as separate arguments
        radial_distance = 0 # TODO
        gnornamize_maximum = 0 # TODO

        xnda = average + 10*gain+100*normalization+1000*output_mode

        debug("RP", normal_mode, thetas.count, phis.count, xnda, thetas.start, phis.start, thetas.delta, phis.delta, radial_distance, gnornamize_maximum)
        self.context.rp_card(normal_mode, thetas.count, phis.count, output_mode, normalization, gain, average, thetas.start, phis.start, thetas.delta, phis.delta, radial_distance, gnornamize_maximum)

    # TODO: shunt admittances, length of transmission line if not straight-line distance
    def transmission_line(self, src, dst, impedance, crossed_line=False, length=None, shunt_admittance_src=0, shunt_admittance_dst=0):
        """ src and dst are (tag_nr, segment_nr) pairs """
        if crossed_line:
            impedance *= -1
        if length is None:
            length = 0
        shunt_admittance_src = complex(shunt_admittance_src)
        shunt_admittance_dst = complex(shunt_admittance_dst)

        debug("TL", src[0], src[1], dst[0], dst[1], impedance, length, shunt_admittance_src.real, shunt_admittance_src.imag, shunt_admittance_dst.real, shunt_admittance_dst.imag)
        self.context.tl_card(src[0], src[1], dst[0], dst[1], impedance, length, shunt_admittance_src.real, shunt_admittance_src.imag, shunt_admittance_dst.real, shunt_admittance_dst.imag)

    # Some simple wrappers for context...
    # TODO: this should be simpler, can't this be auto-generated, or implicitly defined? The best solution is of course to do this in the C++ code,
    # and then the wrappers are immediately correct and nice
    def xq_card(self, *args):
        return self.context.xq_card(*args)
    def get_input_parameters(self, *args):
        return self.context.get_input_parameters(*args)

class geometry_clean(object):
    def __init__(self, geometry):
        self.geometry = geometry

    def wire(self, tag_id, nr_segments, src, dst, radius, length_ratio=1.0, radius_ratio=1.0):
        """ radius is in meter. length_ratio can be set to have non-uniform segment lengths, radius_ratio can be used for tapered wires """
        debug("GW", tag_id, nr_segments, src[0], src[1], src[2], dst[0], dst[1], dst[2], radius) # TODO

        self.geometry.wire(tag_id, nr_segments, src[0], src[1], src[2], dst[0], dst[1], dst[2], radius, length_ratio, radius_ratio)
