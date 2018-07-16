##############################################################################
# V-Ray Tech AOV (Render Elements) creation GUI for Maya
# Version: 1.0.0
# inspired by Bryanna London (https://bryannalondon.com/custom-render-elements/) Original idea and code template goes to him.
# Use:
#     In script editor, enter the code below and execute. Alternatively, middle-mouse drag and drop the code into shelf
#     to make it shelf button.
'''
#from Vray import techAOVs
#reload(techAOVs)
#techAOVs.createTechAOVGUI()
'''
##############################################################################

# import maya command and import mel
import maya.cmds as cmds
import maya.mel as mel

# Create Ambient Occlusion AOV
def createAmboccAOV():
    # select and create a Vray Extra Tex render element
    ambocc = mel.eval('vrayAddRenderElement ExtraTexElement')

    # rename the render element
    ao = cmds.rename(ambocc, 'tech_AO')

    # set explicit channel name to be 'AO'
    cmds.setAttr(ao + '.vray_explicit_name_extratex', 'tech_AO', type='string')

    # set default attribute 'Consider for Anti-Aliasing' off
    cmds.setAttr(ao + '.vray_considerforaa_extratex', 0)

    # create a Vray dirt texture
    vRayDirtTex = cmds.shadingNode('VRayDirt', asTexture=True)

    # create a place2dTexture node
    place2dTextureNode = cmds.shadingNode('place2dTexture', asUtility=True)

    # connect the place2dTexture to VRayDirt
    cmds.connectAttr('%s' % place2dTextureNode + '.outUV', '%s' % vRayDirtTex + '.uvCoord')
    cmds.connectAttr('%s' % place2dTextureNode + '.outUvFilterSize', '%s' % vRayDirtTex + '.uvFilterSize')

    # connect the VrayDirt to AO render element
    cmds.connectAttr('%s' % vRayDirtTex + '.outColor', '%s' % ao + '.vray_texture_extratex', force=True)

# create fresnel AOV
def createFresnelAOV():
    # select and create a Vray Extra Tex render element
    fresnelRE = mel.eval('vrayAddRenderElement ExtraTexElement')
    #print 'ambocc is', ambocc

    # rename the render element
    fresnel = cmds.rename(fresnelRE, 'tech_fresnel')
    #print 'ao is', ao
    #print 'explicit name is:', (maya.cmds.getAttr(ao +'.vray_explicit_name_extratex'))

    # set explicit channel name to be 'AO'
    cmds.setAttr(fresnel + '.vray_explicit_name_extratex', 'tech_fresnel', type='string')

    # set default attribute 'Consider for Anti-Aliasing' off
    cmds.setAttr(fresnel + '.vray_considerforaa_extratex', 0)

    # create a Vray dirt texture
    vRayFresnelTex = cmds.shadingNode('VRayFresnel', asTexture=True)

    # create a place2dTexture node
    place2dTextureNode = cmds.shadingNode('place2dTexture', asUtility=True)

    # connect the place2dTexture to VRayDirt
    cmds.connectAttr('%s' % place2dTextureNode + '.outUV', '%s' % vRayFresnelTex + '.uvCoord')
    cmds.connectAttr('%s' % place2dTextureNode + '.outUvFilterSize', '%s' % vRayFresnelTex + '.uvFilterSize')

    # connect the VrayDirt to AO render element
    cmds.connectAttr('%s' % vRayFresnelTex + '.outColor', '%s' % fresnel + '.vray_texture_extratex', force=True)

# create UV AOV
def createUVAOV():
    # select and create a Vray Extra Tex render element
    uvRE = mel.eval('vrayAddRenderElement ExtraTexElement')

    # rename the render element
    uvPass = cmds.rename(uvRE, 'tech_uv')
    #print 'explicit name is:', (maya.cmds.getAttr(ao +'.vray_explicit_name_extratex'))

    # set explicit channel name to be 'AO'
    cmds.setAttr(uvPass + '.vray_explicit_name_extratex', 'tech_uv', type='string')

    # set default attribute 'Consider for Anti-Aliasing' off
    cmds.setAttr(uvPass + '.vray_considerforaa_extratex', 0)

    # create uRamp
    uRampTex = cmds.shadingNode('ramp', asTexture=True)
    print 'uRampTex is', uRampTex

    # set the created ramp texture from the default V Ramp to be U Ramp
    cmds.setAttr(uRampTex + '.type', 1)

    # set the U Ramp's [1] color entry to be red at position 1 and [0] color entry to be black at position 0
    cmds.setAttr(uRampTex + '.colorEntryList[1].color', 1,0,0, type='double3')
    cmds.setAttr(uRampTex + '.colorEntryList[1].position', 1)
    cmds.setAttr(uRampTex + '.colorEntryList[0].color', 0,0,0, type='double3')
    cmds.setAttr(uRampTex + '.colorEntryList[0].position', 0)

    # create a place2dTexture node for the uRamp
    place2dTextureNode = cmds.shadingNode('place2dTexture', asUtility=True)

    # connect the place2dTexture to U Ramp
    cmds.connectAttr('%s' % place2dTextureNode + '.outUV', '%s' % uRampTex + '.uvCoord')
    cmds.connectAttr('%s' % place2dTextureNode + '.outUvFilterSize', '%s' % uRampTex + '.uvFilterSize')

    # create vRamp
    vRampTex = cmds.shadingNode('ramp', asTexture=True)

    # set the V Ramp's [1] color entry to be green at position 1 and [0] color entry to be black at position 0
    cmds.setAttr(vRampTex + '.colorEntryList[1].color', 0,1,0, type='double3')
    cmds.setAttr(vRampTex + '.colorEntryList[1].position', 1)
    cmds.setAttr(vRampTex + '.colorEntryList[0].color', 0,0,0, type='double3')
    cmds.setAttr(vRampTex + '.colorEntryList[0].position', 0)

    # create a place2dTexture node for the V Ramp
    place2dTextureNode = cmds.shadingNode('place2dTexture', asUtility=True)

    # connect the place2dTexture to V Ramp
    cmds.connectAttr('%s' % place2dTextureNode + '.outUV', '%s' % vRampTex + '.uvCoord')
    cmds.connectAttr('%s' % place2dTextureNode + '.outUvFilterSize', '%s' % vRampTex + '.uvFilterSize')

    # create a plusMinusNode
    plusMinus = cmds.shadingNode('plusMinusAverage', asUtility=True)

    # connect ramps to the plusMinusAverage
    cmds.connectAttr(uRampTex + '.outColor', plusMinus + '.input3D[0]')
    cmds.connectAttr(vRampTex + '.outColor', plusMinus + '.input3D[1]')


    # connect the plusMinus to UV render element
    cmds.connectAttr('%s' % plusMinus + '.output3D', '%s' % uvPass + '.vray_texture_extratex', force=True)

# create rim light AOV
def createRimLightAOV():
    # select and create a Vray Extra Tex render element
    rimLightREinRenderSetting = mel.eval('vrayAddRenderElement ExtraTexElement')

    # rename the render element
    rimLightAOV = cmds.rename(rimLightREinRenderSetting, 'tech_rimLight')

    # set explicit channel name for the AOV
    cmds.setAttr(rimLightAOV + '.vray_explicit_name_extratex', 'tech_rimLight', type='string')

    # set default attribute 'Consider for Anti-Aliasing' off
    cmds.setAttr(rimLightAOV + '.vray_considerforaa_extratex', 0)

    # create a U ramp texture
    rimLightRampTex = cmds.shadingNode('ramp', asTexture=True)
    cmds.setAttr(rimLightRampTex + '.type', 1)

    # set colors for the ramp texgure
    cmds.setAttr(rimLightRampTex+ '.colorEntryList[1].position', 0.485)
    cmds.setAttr(rimLightRampTex + '.colorEntryList[1].color', 0,0,0, type='double3')
    cmds.setAttr(rimLightRampTex+ '.colorEntryList[2].position', 0.1)
    cmds.setAttr(rimLightRampTex + '.colorEntryList[2].color', 0.85,0.85,0.85, type='double3')
    cmds.setAttr(rimLightRampTex+ '.colorEntryList[3].position', 0)
    cmds.setAttr(rimLightRampTex + '.colorEntryList[3].color', 1,1,1, type='double3')

    # create a samplerInfo node
    samplerInfoNode = cmds.shadingNode('samplerInfo', asUtility=True)

    # connect the place2dTexture to the U ramp
    cmds.connectAttr(samplerInfoNode + '.facingRatio', rimLightRampTex + '.uCoord')
    cmds.connectAttr(samplerInfoNode + '.facingRatio', rimLightRampTex + '.vCoord')

    # connect the VrayDirt to AO render element
    cmds.connectAttr(rimLightRampTex + '.outColor', rimLightAOV + '.vray_texture_extratex', force=True)

# create position world AOV
def createPositionWorldAOV():
    # create a Vray Extra Tex render element
    positionWorldREinRenderSetting = mel.eval('vrayAddRenderElement ExtraTexElement')

    # rename the render element
    positionWorldAOV = cmds.rename(positionWorldREinRenderSetting, 'tech_pWorld')
    #print 'explicit name is:', (maya.cmds.getAttr(ao +'.vray_explicit_name_extratex'))

    # set explicit channel name to be 'AO'
    cmds.setAttr(positionWorldAOV + '.vray_explicit_name_extratex', 'tech_pWorld', type='string')

    # set default attribute 'Consider for Anti-Aliasing' off
    cmds.setAttr(positionWorldAOV + '.vray_considerforaa_extratex', 0)

    # create a samplerInfo node
    samplerInfoNode = cmds.shadingNode('samplerInfo', asUtility=True)

    # connect the place2dTexture to the U ramp
    cmds.connectAttr(samplerInfoNode + '.pointWorldX', positionWorldAOV + '.vray_texture_extratexR', force=True)
    cmds.connectAttr(samplerInfoNode + '.pointWorldY', positionWorldAOV + '.vray_texture_extratexG', force=True)
    cmds.connectAttr(samplerInfoNode + '.pointWorldZ', positionWorldAOV + '.vray_texture_extratexB', force=True)

# create TopDown AOV
def createTopDownAOV():
    # create a Vray Extra Tex render element
    topDownREinRenderSetting = mel.eval('vrayAddRenderElement ExtraTexElement')

    # rename the render element
    topDownAOV = cmds.rename(topDownREinRenderSetting, 'tech_topDown')
    #print 'explicit name is:', (maya.cmds.getAttr(ao +'.vray_explicit_name_extratex'))

    # set explicit channel name to be 'AO'
    cmds.setAttr(topDownAOV + '.vray_explicit_name_extratex', 'tech_topDown', type='string')

    # set default attribute 'Consider for Anti-Aliasing' off
    cmds.setAttr(topDownAOV + '.vray_considerforaa_extratex', 0)

    # create a vrayFalloffTex node
    vrayFalloffTexNode = mel.eval('vrayCreateNodeFromDll ("topdown_tex", "texture", "TexFalloff", 2);')

    # set default attributes
    cmds.setAttr(vrayFalloffTexNode + '.direction_type', 2)
    cmds.setAttr(vrayFalloffTexNode + '.color1', 1, 0, 0)
    cmds.setAttr(vrayFalloffTexNode + '.color2', 0, 1, 0)

    # connect the place2dTexture to the U ramp
    cmds.connectAttr(vrayFalloffTexNode + '.outColor', topDownAOV + '.vray_texture_extratex', force=True)

# create wireframe AOV
def createWireframeAOV():
    # create a Vray Extra Tex render element
    wireframeREinRenderSetting = mel.eval('vrayAddRenderElement ExtraTexElement')

    # rename the render element
    wireframeAOV = cmds.rename(wireframeREinRenderSetting, 'tech_wireframe')
    #print 'explicit name is:', (maya.cmds.getAttr(ao +'.vray_explicit_name_extratex'))

    # set explicit channel name to be 'AO'
    cmds.setAttr(wireframeAOV + '.vray_explicit_name_extratex', 'tech_wireframe', type='string')

    # set default attribute 'Consider for Anti-Aliasing' off
    cmds.setAttr(wireframeAOV + '.vray_considerforaa_extratex', 0)

    # create a vrayEdgesTex node
    vrayEdgesTexNode = cmds.shadingNode('VRayEdges', asTexture=True)

    # set default attributes
    cmds.setAttr(vrayEdgesTexNode + '.pixelWidth', .1)

    # create a place2dTexture node
    place2dTexNode = cmds.shadingNode('place2dTexture', asUtility=True)

    # connect the place2dTexture to the VrayEdges Tex
    cmds.connectAttr(place2dTexNode + '.outUV', vrayEdgesTexNode + '.uvCoord')
    cmds.connectAttr(place2dTexNode + '.outUvFilterSize', vrayEdgesTexNode + '.uvFilterSize')

    # connect the place2dTexture to the U ramp
    cmds.connectAttr(vrayEdgesTexNode + '.outColor', wireframeAOV + '.vray_texture_extratex', force=True)

# create curvature AOV
def createCurvatureAOV():
    # create a Vray Extra Tex render element
    curvatureREinRenderSetting = mel.eval('vrayAddRenderElement ExtraTexElement')

    # rename the render element
    curvatureAOV = cmds.rename(curvatureREinRenderSetting, 'tech_curvature')
    #print 'explicit name is:', (maya.cmds.getAttr(ao +'.vray_explicit_name_extratex'))

    # set explicit channel name to be 'AO'
    cmds.setAttr(curvatureAOV + '.vray_explicit_name_extratex', 'tech_curvature', type='string')

    # set default attribute 'Consider for Anti-Aliasing' off
    cmds.setAttr(curvatureAOV + '.vray_considerforaa_extratex', 0)

    # create a vrayEdgesTex node
    vrayCurvatureTexNode = cmds.shadingNode('VRayCurvature', asTexture=True)

    # connect the place2dTexture to the U ramp
    cmds.connectAttr(vrayCurvatureTexNode + '.outColor', curvatureAOV + '.vray_texture_extratex', force=True)


### create GUI

# if an existing customAOVWindow exists, delete it before creating a new one
if cmds.window('customAOVWindow', exists=True):
    cmds.deleteUI('customAOVWindow')

def createTechAOVGUI():

    customAOVWindow = cmds.window( 'customAOVWindow', title="Create Tech AOVs", iconName='Tech AOV', widthHeight=(300, 200) )
    # print 'current customAOVWindow is:', customAOVWindow
    cmds.columnLayout( adjustableColumn=True )

    cmds.checkBox('occlusion', label='Occlusion', value=False)
    cmds.checkBox('fresnel', label='Fresnel', value=False)
    cmds.checkBox('uv', label='uv', value=False)
    cmds.checkBox('rim_light', label='Rim Light', value=False)
    cmds.checkBox('position_world', label='position world', value=False)
    cmds.checkBox('top_down', label='Top Down', value=False )
    cmds.checkBox('wireframe', label='Wireframe', value=False )
    cmds.checkBox('curvature', label='curvature', value=False )

    cmds.button(label='Run', command=queryValues)
    cmds.button(label='Close', command=closeWindow)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.showWindow('customAOVWindow')

# function for when pressing the 'Run' button to query checkbox value
def queryValues(*args):
    occlusionAOVValue = cmds.checkBox('occlusion', query=True, value=False)
    fresnelAOVValue = cmds.checkBox('fresnel', query=True, value=False)
    uvAOVValue = cmds.checkBox('uv', query=True, value=False)
    rimLightAOVValue = cmds.checkBox('rim_light', query=True, value=False)
    pWorldAOVValue = cmds.checkBox('position_world', query=True, value=False)
    topDownAOVValue = cmds.checkBox('top_down', query=True, value=False)
    wireframeAOVValue = cmds.checkBox('wireframe', query=True, value=False)
    curvatureAOVValue = cmds.checkBox('curvature', query=True, value=False)

    # when no AOV is ticked for creation, send a reminder to users
    if not occlusionAOVValue and not fresnelAOVValue and not uvAOVValue and not rimLightAOVValue and not pWorldAOVValue and not topDownAOVValue and not wireframeAOVValue and not curvatureAOVValue:
        # if no custom AOV is ticked for creation, run the showReminder() command to pop up a reminder to users
        showReminder()
        print 'no tech AOV is created'
    if occlusionAOVValue:
        createAmboccAOV()
    if fresnelAOVValue:
        createFresnelAOV()
    if uvAOVValue:
        createUVAOV()
    if rimLightAOVValue:
        createRimLightAOV()
    if pWorldAOVValue:
        createPositionWorldAOV()
    if topDownAOVValue:
        createTopDownAOV()
    if wireframeAOVValue:
        createWireframeAOV()
    if curvatureAOVValue:
        createCurvatureAOV()

# function to show a reminder window for when no tech AOV is ticked for creation
def showReminder():
    reminderWindow = cmds.window('reminderWindow',title="Reminder", iconName='Short Name', widthHeight=(200, 55), resizeToFitChildren=True )
    cmds.columnLayout( adjustableColumn=True )
    # note: need to work on the text style to make it more obvious
    cmds.text(label='No Tech AOV is set to create' )
    cmds.button(label='OK', command=closeReminderWindow)
    cmds.setParent( '..' )
    cmds.showWindow( reminderWindow )

def closeReminderWindow(*args):
    from maya import cmds
    cmds.deleteUI('reminderWindow', window=True)

def closeWindow(*args):
    from maya import cmds
    cmds.deleteUI('customAOVWindow', window=True)

# to run the script directly from Maya's script editor, uncommnet the line below, copy/paste the whole script into 
# Maya script editor and execute it
# createTechAOVGUI()




