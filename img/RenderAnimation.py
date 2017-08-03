import bpy
from math import radians

name = 'walk'
length = 48

dir = '/home/nicola/Documents/code/python/2dgame/img/person/'+name+'/'
rotObj = bpy.data.objects['Rotation']
rotation = 180
frame = 0

#bpy.context.scene.frame_set(frame)

for n in range(5):
    rotObj.rotation_euler = (0, 0, radians(rotation))
    for i in range(length+1):
        bpy.context.scene.frame_set(i)
        bpy.context.scene.render.filepath = dir+str(n)+'-'+str(i)+'f.png'
        bpy.ops.render.render(write_still=True, layer="Main")
        bpy.context.scene.render.filepath = dir+str(n)+'-'+str(i)+'b.png'
        bpy.ops.render.render(write_still=True, layer="Shadow")
        
        
    rotation -= 45

'''
ls = bpy.context.scene.render.layers
for l in ls:
            for l2 in ls:
                l2.use = False
            l.use = True
            bpy.ops.render.render(write_still=True)
'''