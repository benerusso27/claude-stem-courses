# Alt text — Lab 9: Columns

Each entry is embedded in the SVG `<title>`/`<desc>` and in the Word file's image description.

## fig1_setup (.svg / .png)
**Figure 1. Test set-up**

Three panels. (a) The strut frame: a bar stands vertically between two knife edges seated in V-blocks, the upper one under a loading screw in the crosshead and the lower one on a load cell. The bar is drawn bowed to the right (exaggerated). The load P acts downward at the top end A; B is the bottom end; L is the distance between the pivots. A dial gage touches the bar at mid-length on the right (convex, front) side, and strain gages are bonded at mid-length on the front and back faces. Beer's axes are shown: x pointing down the column from A and y pointing to the right. (b) The end fixtures: a knife-edge holder with three V-grooves at offsets of 0, 1 and 2 mm from the axis, used for Parts A and C, and a clamp block that grips 40 mm of the bar between two jaws, used for Part B and Part D. (c) The 25.4 by 6.35 mm cross-section seen along the column: it bends across the 6.35 mm thickness t, in the y direction, with the front gage F on the convex face and the back gage B on the opposite face; the radius of gyration is t over the square root of 12.

## fig2_ends (.svg / .png)
**Figure 2. End conditions and effective lengths**

Five columns of equal length L, each drawn with its first buckling mode computed from this lab's closed-form solutions and loaded by P at the top. Purple dots mark points of zero bending moment (inflection points) and purple brackets mark the effective length L_e, the length of an equivalent pinned column. Pinned at both ends: a half sine, K = 1. Pinned top, fixed bottom: the inflection point lies 0.699 L below the pin, K = 0.699. Fixed at both ends: inflection points at the quarter points, K = 0.5. Free top, fixed bottom: the shape continued as its mirror image below the base forms a pinned column of length 2 L, K = 2. Clamps of finite stiffness, with k L over EI equal to 45 as in Part B: the shape is between the pinned and fixed cases and K = 0.52.

## fig3_southwell (.svg / .png)
**Figure 3. Imperfect columns and the Southwell plot**

Two panels in nondimensional form. (a) Load ratio P over P_cr against the mid-length deflection divided by the imperfection. A column with an initial bow delta_0 follows alpha over (1 minus alpha), and a column with a load offset e follows the secant result (Eq. 10.31); both rise steeply at first and then flatten, approaching P over P_cr = 1 without reaching it. The perfect column stays straight up to P_cr and then deflects at constant load (dashed). (b) The same bowed-column readings plotted as deflection over load against deflection fall on a straight line whose slope is 1 over P_cr and whose intercept is delta_0 over P_cr, so P_cr and the equivalent bow follow from readings taken well below the critical load.

## fig4_eccentric (.svg / .png)
**Figure 4. Eccentric loads and the secant formula**

Two panels. (a) The lever arm of the load about the mid-length section, divided by the eccentricity e, against P over P_cr: the secant result rises from 1 at no load to about 2 at half the critical load and without bound as P approaches P_cr; the simpler amplification factor 1 over (1 minus alpha) is close to it; the dashed line at 1 is what superposition without deflection (Eq. 4.58 or Eq. 10.37) assumes. (b) For 6061-T6, the load at first yield divided by P_cr against the eccentricity ratio e c over r squared, for slenderness ratios of 50, 100 and 250. For the slender column (250) the first-yield load stays just below P_cr however small the eccentricity, while the linear estimate (thin lines) runs far above P_cr; for the stocky column (50) eccentricity lowers the load strongly and the two estimates are close.

## fig5_curve (.svg / .png)
**Figure 5. Column curve for 6061-T6**

Critical stress against effective slenderness ratio for 6061-T6 aluminum, from 0 to 350. Euler's hyperbola rises without limit as the slenderness falls and crosses the yield strength (a horizontal line at about 274 MPa) near L_e/r = 50; the region to the left is shaded because there Euler predicts a stress the material cannot carry. The tangent-modulus curve, from Lab 1's stress-strain curve, leaves Euler's hyperbola below about L_e/r = 60 and stays under the yield strength until very short columns; the reduced-modulus curve lies slightly above it. The Aluminum Association allowable-stress curve (with its factor of safety) runs well below both. Tick marks along the bottom show the slenderness of this lab's tests: Part D at about 49, the 300 mm pinned bar and the ideal fixed-fixed 600 mm bar at about 164, the ideal fixed-pinned 640 mm bar near 244, the 450 mm bar of Parts A and C at about 245, and the 600 mm pinned bar at about 327.
