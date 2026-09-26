import numpy as np

class BraneworldGravitySimulation:
    """
    Simulates modified gravitational potentials under Randall-Sundrum (RS-II) 
    braneworld models within the Aura .xsim environmental framework.
    """
    def __init__(self, bulk_curvature_scale_m: float = 1e-4, gravitational_constant: float = 6.67430e-11):
        self.ell = bulk_curvature_scale_m  # Bulk curvature radius (meters)
        self.G = gravitational_constant   # Newton's gravitational constant
        
    def modified_potential(self, mass: float, r_array: np.ndarray) -> np.ndarray:
        """
        Calculates the RS braneworld gravitational potential V(r):
        V(r) = (G * M / r) * (1 + (ell^2 / r^2))
        """
        # Prevent division by zero at r=0
        r_safe = np.where(r_array == 0, 1e-12, r_array)
        
        newtonian_term = (self.G * mass) / r_safe
        rs_correction = 1.0 + (self.ell**2 / r_safe**2)
        
        return newtonian_term * rs_correction

    def force_deviation_ratio(self, r_array: np.ndarray) -> np.ndarray:
        """
        Computes the ratio of braneworld force deviation compared to standard Newtonian gravity.
        Ratio = F_brane / F_newton = 1 + 3*(ell^2 / r^2) [derived from negative gradient of V(r)]
        """
        r_safe = np.where(r_array == 0, 1e-12, r_array)
        return 1.0 + 3.0 * (self.ell**2 / r_safe**2)

# --- Execution Example for the Pipeline ---
if __name__ == "__main__":
    # Initialize simulator with a sub-millimeter bulk scale parameter
    sim = BraneworldGravitySimulation(bulk_curvature_scale_m=5e-5)
    
    # Test across micro-scales (1 micrometer to 1 millimeter)
    radii = np.logspace(-6, -3, 100) # distances in meters
    stellar_mass = 2.0 * 1.989e30    # 2 Solar Masses (Neutron Star scale)
    
    potentials = sim.modified_potential(stellar_mass, radii)
    deviations = sim.force_deviation_ratio(radii)
    
    print(f"Aura .xsim Module Initialized successfully.")
    print(f"Target Bulk Curvature Radius ($\ell$): {sim.ell * 1e6} microns")
    print(f"Max Force Deviation Ratio at r = {radii[0]*1e6:.1f} µm: {deviations[0]:.4f}x")
