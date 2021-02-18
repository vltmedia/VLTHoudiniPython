# Description
These are HDAs and tools for use in Houdini 18.5+

# Octane Material Converter
With the Octane Material Converter HDA, an artist can convert Principled Shader  materials straight into Octane Materials. All the artist needs to do is:

1. Plug in your geometry with a Principled Shader Material into **Input 1**
2. Click the **Process Materials** button to create NEW Octane materials based on the Principle Material's textures and settings.
3. The output of the HDA node will have the new Octane Materials set properly.

Be advised that every time you click the button, the Octane Materials previously generated will be deleted, unless you change their names and resave.

80% of the parameters and textures are supported during conversion. Subsurface compatibility will be added in the future. 
![OctaneMaterialConverter-Window](https://vltmediablog.ml/content/images/2021/02/OctaneMaterialConverter-Window.png)

[Video](https://www.dropbox.com/s/yga5n09okkhvy8u/210217-HoudiniHDA-OctaneMaterialConverter.mp4?raw=1)


# Mass Importer
With the Mass Importer HDA, an artist can import multiple geometry files into Houdini, then split them up into:
- A new Subnet
- Individual nodes at the /obj root location
- Individual nodes in the same parent node as the HDA was executed from

The HDA includes a file pattern parser that can traverse a directory and import the appropriate files.
We've been using this HDA heavily in conjunction with Physics Painter.

![MassImport-Preview](https://vltmediablog.ml/content/images/2021/02/MassImport-Preview.png)
![MassImport](https://vltmediablog.ml/content/images/2021/02/MassImport.png)

[Video](https://www.dropbox.com/s/8hjlwwwkgqktu31/210217-HoudiniHDA-MassImporter.mp4?raw=1)