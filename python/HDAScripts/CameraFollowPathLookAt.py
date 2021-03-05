def EnableConstraints(kwargs):
    nodee = kwargs["node"]
    nodee.parm("constraints_on").set(nodee.evalParm('Enable'))
    nodee.parm("constraints_path").set("constraints")
    print("Just set to:  " + str(nodee.evalParm('Enable')))
    