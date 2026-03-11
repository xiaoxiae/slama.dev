/**********************************************************/
/* Malolo's screw-less / snap fit Raspberry Pi 4 Model B  */
/* Case                                                   */
/**********************************************************/
/*                                                        */
/* Use this generator to customize your Raspberry Pi case */
/* according to your needs.                               */
/*                                                        */
/**********************************************************/
/*                                                        */
/* Visit me on Thingiverse: :                             */
/*   -> https://www.thingiverse.com/Malolo                */
/*                                                        */
/**********************************************************/

/**********************************************************/
/* Configuration                                          */
/**********************************************************/

/* [Case Style] */

// Bottom

Bottom_Style = "None"; // [base:Pain/Solid, hex_sm:Hexagons - Single Material, hex_mm2:Hexagons - Two Materials, slots_sm:Slots - Single Material, mesh_sm:Mesh - Single Material]

/**********************************************************/
/* Case Generation                                        */
/**********************************************************/

case_mesh();

/**********************************************************/
/* Modules                                                */
/**********************************************************/

module case_mesh(case_name) {
    
    difference() {
        
        import("z_bottom_base_sm.stl");
        
        if (Bottom_Style == "hex_sm") {
            
            import("z_bottom_style_hex_sm_cut.stl");
            
        } else if (Bottom_Style == "hex_mm2") {
            
            import("z_bottom_style_hex_mm2_c1_cut.stl");
            
        } else if (Bottom_Style == "slots_sm") {
            
            import("z_bottom_style_slots_sm_cut.stl");
            
        } else if (Bottom_Style == "mesh_sm") {
            
            import("z_bottom_style_mesh_sm_cut.stl");
            
        }
        
    }
}