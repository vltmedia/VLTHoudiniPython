def loadPreset(kwargs):
    presets = [{
                "PresetName": "Sin Wave",
                "Freq_": 0.5
               },{
                "PresetName": "Cosin Wave",
                "Freq_": 1.2
               },{
                "PresetName": "Hearbeat Wave",
                "Freq_": 0.2
               },
               
              ]


    node = kwargs['node']
    parm = node.parm('Wave_Shape2')
    i = parm.eval()
    # print("chosen | ",i)
    node.setParms(presets[i])
    
def loadWaveShape(kwargs, id):
    presets = [{
                "PresetName": "Sin Wave",
                "Freq_": 0.5
               },{
                "PresetName": "Cosin Wave",
                "Freq_": 1.2
               },{
                "PresetName": "Hearbeat Wave",
                "Freq_": 0.2
               },
               
              ]


    node = kwargs['node']
    i = id
    # print("chosen | ",i)
    node.setParms(presets[i])
    
def loadPresetCustom(kwargs):
    presets = [{
               "Wave_Shape2": 0,
        
                "sin_min3": 0.182,
                "Freq_": 0.5,
                "Multiplierx": 1,
               "Multipliery": 1,
               "Multiplierz": 1,
               },{
               "Wave_Shape2": 2,
               "length": 0.054,
               "frequency3": 2.3484,
               "offset_speed3": 0.1558,
               "position_multiplier3x": 0.01,
               "position_multiplier3y": 0.034,
               "position_multiplier3z": 0.034,
               "sin_min3": 0.182,
               "out_max3": 1,
                "out_min3": -6.2
                ,
               "frequency2": 1.0499,
               "position_multiplier2x": 0.083,
               "position_multiplier2y": 0.005,
               "Multiplierx": 1,
               "Multipliery": 1,
               "Multiplierz": 1,
               "position_multiplier2z":  -0.095

                
               }
               
              ]

    node = kwargs['node']
    parm = node.parm('Preset')
    # print(node.parms())
    i = parm.eval()
    # print("chosen | ",presets[i])
    
        
    node.setParms(presets[i])
    loadWaveShape(kwargs, presets[i]['Wave_Shape2'])