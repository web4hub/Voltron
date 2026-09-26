import numpy as np
import matplotlib.pyplot as plt

class BraneworldGravitySimulation:
    """
    Simulates modified gravitational force ratios under Randall-Sundrum (RS-II) 
    braneworld models within the Aura .xsim environmental framework.
    """
    def __init__(self, bulk_curvature_scale_m: float = 5e-5, gravitational_constant: float = 6.67430e-11):
        self.ell = bulk_curvature_scale_m  # Bulk curvature radius (meters, e.g., 50 microns)
        self.G = gravitational_constant   # Newton's gravitational constant
        
    def force_deviation_ratio(self, r_array: np.ndarray) -> np.ndarray:
        """
        Computes the ratio of braneworld force deviation compared to standard Newtonian gravity:
        F_brane / F_newton = 1 + 3 * (ell^2 / r^2)
        """
        r_safe = np.where(r_array == 0, 1e-12, r_array)
        return 1.0 + 3.0 * (self.ell**2 / r_safe**2)

if __name__ == "__main__":
    # Initialize simulator with a 50-micron bulk scale parameter
    sim = BraneworldGravitySimulation(bulk_curvature_scale_m=5e-5)
    
    # Test across micro-scales (1 micrometer to 1 millimeter)
    radii = np.logspace(-6, -3, 500) # distance in meters
    radii_microns = radii * 1e6     # convert to microns for clean plotting
    
    deviations = sim.force_deviation_ratio(radii)
    
    # Plotting configuration
    plt.figure(figsize=(10, 6))
    plt.plot(radii_microns, deviations, label=r'Randall-Sundrum ($\ell = 50\,\mu\text{m}$)', color='#7b2cbf', lw=2.5)
    plt.axhline(y=1.0, color='#6c757d', linestyle='--', label='Standard Newtonian Baseline (GR)')
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Separation Distance $r$ ($\mu\text{m}$)', fontsize=12)
    plt.ylabel('Force Ratio ($F_{\text{brane}} / F_{\text{Newton}}$)', fontsize=12)
    plt.title('Short-Range Gravitational Force Spike in Braneworld Models', fontsize=14, fontweight='bold')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=11, loc='upper right')
    plt.tight_layout()
    
    # Save output for logging telemetry or presentation
    plt.savefig('simulations/braneworld_gravity_spike.png', dpi=300)
    plt.show()
    print("Simulation plot generated and saved successfully to simulations/braneworld_gravity_spike.png")
