"""
Solves, then animates solution to the Lorenz oscillator.
"""

import Initial_Value_Problems as ivp
import manim as mn
import numpy as np
import math

class LorenzOscillatorTime(mn.Scene):
    def construct(self):
        #Describe and solve IVP
        #------------------------------
        s = 10
        p = 28
        b = 8/3
        f = lambda t,u: np.array([s * (u[1] - u[0]), u[0] * (p - u[2]) - u[1], u[0] * u[1] - b * u[2]])
        u_0 = np.array([1., 1., 1.])
        
        
        #Parameters for numerical integration
        dt = 0.001
        t_final = 30
        method = "equal_rk4"

        
        #Run the algorithm, but don't plot, just return solution
        u_list = ivp.solve_ivp(f, u_0, dt, t_final, method, [], [])
        u0_list = [u[0] for u in u_list]
        u1_list = [u[1] for u in u_list]
        u2_list = [u[2] for u in u_list]
        #------------------------------
        
        
        #Setup animation
        #------------------------------
        #Construct the coordinate axes
        axes0 = mn.Axes(x_range = [0, t_final, t_final / 10],
                        y_range = [min(u0_list), max(u0_list), (max(u0_list) - min(u0_list)) / 10],
                        x_length = 4,
                        y_length = 4,                     
                        tips = False)
        axes0.shift(mn.LEFT * 4.5)

        
        axes1 = mn.Axes(x_range = [0, t_final, t_final / 10],
                        y_range = [min(u1_list), max(u1_list), (max(u1_list) - min(u1_list)) / 10],
                        x_length = 4,
                        y_length = 4,
                        tips = False)
                        
                        
        axes2 = mn.Axes(x_range = [0, t_final, t_final / 10],
                        y_range = [min(u2_list), max(u2_list), (max(u2_list) - min(u2_list)) / 10],
                        x_length = 4,
                        y_length = 4,
                    tips = False)              
        axes2.shift(mn.RIGHT * 4.5)
        
        
        axes = mn.VGroup()
        axes += axes0
        axes += axes1
        axes += axes2
        
        
        #Add labels
        labels = mn.VGroup()
        labels += axes0.get_x_axis_label(mn.Tex(r"$t$", font_size = 24), edge = mn.RIGHT, direction = mn.RIGHT)
        labels += axes0.get_y_axis_label(mn.Tex(r"$x$", font_size = 24), edge = mn.LEFT, direction = mn.LEFT)
        labels += axes1.get_x_axis_label(mn.Tex(r"$t$", font_size = 24), edge = mn.RIGHT, direction = mn.RIGHT)
        labels += axes1.get_y_axis_label(mn.Tex(r"$y$", font_size = 24), edge = mn.LEFT, direction = mn.LEFT)
        labels += axes2.get_x_axis_label(mn.Tex(r"$t$", font_size = 24), edge = mn.RIGHT, direction = mn.RIGHT)
        labels += axes2.get_y_axis_label(mn.Tex(r"$z$", font_size = 24), edge = mn.LEFT, direction = mn.LEFT)
        
        
        #Add functions to plot
        def x(t):
            """
            Solution to x interpolated from list of points.
            """
            i = t / dt
            if i <= len(u0_list) - 1:
                if i == int(i): #i is integer
                    return u0_list[int(i)]
                else: #i isn't integer, interpolate between nearest points
                    return u0_list[math.ceil(i)] * math.modf(i)[0] + u0_list[math.floor(i)] * (1 - math.modf(i)[0])   
        
        
        def y(t):
            """
            Solution to y interpolated from list of points.
            """
            i = t / dt
            if i <= len(u1_list) - 1:
                if i == int(i): #i is integer
                    return u1_list[int(i)]
                else: #i isn't integer, interpolate between nearest points
                    return u1_list[math.ceil(i)] * math.modf(i)[0] + u1_list[math.floor(i)] * (1 - math.modf(i)[0])


        def z(t):
            """
            Solution to z interpolated from list of points.
            """
            i = t / dt
            if i <= len(u2_list) - 1:
                if i == int(i): #i is integer
                    return u2_list[int(i)]
                else: #i isn't integer, interpolate between nearest points
                    return u2_list[math.ceil(i)] * math.modf(i)[0] + u2_list[math.floor(i)] * (1 - math.modf(i)[0])
        
        
        functions = mn.VGroup()  #Stores functions to plot
        functions += axes0.plot(x, x_range = [0, t_final], color = mn.BLUE)
        functions += axes1.plot(y, x_range = [0, t_final], color = mn.GREEN)
        functions += axes2.plot(z, x_range = [0, t_final], color = mn.RED)
        
        
        #Construct objects unrelated to animation (initial setup)
        self.add(axes, labels, functions)
        #------------------------------
        
        
        #Make the animation
        #------------------------------
        #Make objects for the animation
        e = mn.ValueTracker(0.01) #parameter is start time
        
        x_line_anim = mn.always_redraw(lambda : axes0.plot(x, x_range = [0, e.get_value()], color = mn.WHITE))
        x_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(axes0.c2p(e.get_value(), x(e.get_value()))))
        
        y_line_anim = mn.always_redraw(lambda : axes1.plot(y, x_range = [0, e.get_value()], color = mn.WHITE))
        y_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(axes1.c2p(e.get_value(), y(e.get_value()))))
        
        z_line_anim = mn.always_redraw(lambda : axes2.plot(z, x_range = [0, e.get_value()], color = mn.WHITE))
        z_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(axes2.c2p(e.get_value(), z(e.get_value()))))
        
        
        #Construct objects for animation
        self.add(x_line_anim, x_dot_anim, y_line_anim, y_dot_anim, z_line_anim, z_dot_anim)
        
        
        #Make the animation
        self.wait(2)
        self.play(e.animate.set_value(t_final), run_time = 30)
        self.wait(2)
        #------------------------------
        
        
class LorenzOscillatorPhase(mn.Scene):
    def construct(self):
        #Describe and solve IVP
        #------------------------------
        s = 10
        p = 28
        b = 8/3
        f = lambda t,u: np.array([s * (u[1] - u[0]), u[0] * (p - u[2]) - u[1], u[0] * u[1] - b * u[2]])
        u_0 = np.array([1., 1., 1.])
        
        
        #Parameters for numerical integration
        dt = 0.001
        t_final = 30
        method = "equal_rk4"


        #Run the algorithm, but don't plot, just return solution
        u_list = ivp.solve_ivp(f, u_0, dt, t_final, method, [], [])
        u0_list = [u[0] for u in u_list]
        u1_list = [u[1] for u in u_list]
        u2_list = [u[2] for u in u_list]
        #------------------------------
        
        
        #Setup animation
        #------------------------------
        #x-y projection
        axes0 = mn.Axes(x_range = [min(u0_list), max(u0_list), (max(u0_list) - min(u0_list)) / 10],
                        y_range = [min(u1_list), max(u1_list), (max(u1_list) - min(u1_list)) / 10],
                        x_length = 4,
                        y_length = 4,                     
                        tips = False)
        axes0.shift(mn.LEFT * 4.5)
                        
        #x-z projection               
        axes1 = mn.Axes(x_range = [min(u0_list), max(u0_list), (max(u0_list) - min(u0_list)) / 10],
                        y_range = [min(u2_list), max(u2_list), (max(u2_list) - min(u2_list)) / 10],
                        x_length = 4,
                        y_length = 4,                     
                        tips = False)  
                        
        #y-z projection              
        axes2 = mn.Axes(x_range = [min(u1_list), max(u1_list), (max(u1_list) - min(u1_list)) / 10],
                        y_range = [min(u2_list), max(u2_list), (max(u2_list) - min(u2_list)) / 10],
                        x_length = 4,
                        y_length = 4,                     
                        tips = False)   
        axes2.shift(mn.RIGHT * 4.5)
        
        
        axes = mn.VGroup()
        axes += axes0
        axes += axes1
        axes += axes2
       
       
        #Add labels 
        labels = mn.VGroup()
        labels += axes0.get_x_axis_label(mn.Tex(r"$x$", font_size = 24), edge = mn.RIGHT)
        labels += axes0.get_y_axis_label(mn.Tex(r"$y$", font_size = 24), edge = mn.UP)
        labels += axes1.get_x_axis_label(mn.Tex(r"$x$", font_size = 24), edge = mn.RIGHT)
        labels += axes1.get_y_axis_label(mn.Tex(r"$z$", font_size = 24), edge = mn.UP)
        labels += axes2.get_x_axis_label(mn.Tex(r"$y$", font_size = 24), edge = mn.RIGHT)
        labels += axes2.get_y_axis_label(mn.Tex(r"$z$", font_size = 24), edge = mn.UP)
        
        
        #Add functions to plot
        def x(t):
            """
            Solution to x interpolated from list of points.
            """
            i = t / dt
            if i <= len(u0_list) - 1:
                if i == int(i): #i is integer
                    return u0_list[int(i)]
                else: #i isn't integer, interpolate between nearest points
                    return u0_list[math.ceil(i)] * math.modf(i)[0] + u0_list[math.floor(i)] * (1 - math.modf(i)[0])
        
        
        def y(t):
            """
            Solution to y interpolated from list of points.
            """
            i = t / dt
            if i <= len(u1_list) - 1:
                if i == int(i): #i is integer
                    return u1_list[int(i)]
                else: #i isn't integer, interpolate between nearest points
                    return u1_list[math.ceil(i)] * math.modf(i)[0] + u1_list[math.floor(i)] * (1 - math.modf(i)[0])


        def z(t):
            """
            Solution to z interpolated from list of points.
            """
            i = t / dt
            if i <= len(u2_list) - 1:
                if i == int(i): #i is integer
                    return u2_list[int(i)]
                else: #i isn't integer, interpolate between nearest points
                    return u2_list[math.ceil(i)] * math.modf(i)[0] + u2_list[math.floor(i)] * (1 - math.modf(i)[0])
        
        
        def xy(t):
            """
            Paramemtric function for (x,y)
            """
            return [x(t), y(t), 0]
            
            
        def xz(t):
            """
            Parametric function for (x,z)
            """
            return [x(t), z(t), 0]
            
            
        def yz(t):
            """
            Parametric function for (y,z)
            """
            return [y(t), z(t), 0]
        
        
        f_xy = axes0.plot_parametric_curve(lambda t: xy(t), t_range = [0, t_final], color = mn.BLUE)
        f_xz = axes1.plot_parametric_curve(lambda t: xz(t), t_range = [0, t_final], color = mn.BLUE)
        f_yz = axes2.plot_parametric_curve(lambda t: yz(t), t_range = [0, t_final], color = mn.BLUE)
        
        
        functions = mn.VGroup()  #Stores functions to plot
        functions += f_xy
        functions += f_xz
        functions += f_yz
        
        
        #Construct objects unrelated to animation (initial setup)
        self.add(axes, labels, functions)
        #------------------------------
        
        
        #Make the animation
        #------------------------------
        #Make objects for the animation
        e = mn.ValueTracker(0.01) #parameter is start time
        
        lines = mn.VGroup()
        dots = mn.VGroup()
        
        xy_line_anim = mn.always_redraw(lambda : axes0.plot_parametric_curve(lambda t: xy(t), t_range = [0, e.get_value()], color = mn.WHITE))
        xz_line_anim = mn.always_redraw(lambda : axes1.plot_parametric_curve(lambda t: xz(t), t_range = [0, e.get_value()], color = mn.WHITE))
        yz_line_anim = mn.always_redraw(lambda : axes2.plot_parametric_curve(lambda t: yz(t), t_range = [0, e.get_value()], color = mn.WHITE))
        
        xy_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.RED).move_to(axes0.c2p(x(e.get_value()), y(e.get_value()))))
        xz_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.RED).move_to(axes1.c2p(x(e.get_value()), z(e.get_value()))))
        yz_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.RED).move_to(axes2.c2p(y(e.get_value()), z(e.get_value()))))
        
        lines += xy_line_anim 
        lines += xz_line_anim
        lines += yz_line_anim
        
        dots += xy_dot_anim
        dots += xz_dot_anim
        dots += yz_dot_anim
        
        
        #Construct objects for animation
        self.add(lines, dots)
        
        
        #Make the animation
        self.wait(2)
        self.play(e.animate.set_value(t_final), run_time = 30)
        self.wait(2)
        #------------------------------