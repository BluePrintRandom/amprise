import bpy, bge, math
import wave
from array import array
from mathutils import Vector

# Save packed sound to disk, so we can load with wave
# (BGE api doesn't provide access to the raw data - as far as I know):
bpy.ops.file.unpack_all(method="USE_ORIGINAL")

# Even worse, there seems to be no way to get the wav name from the
# actuator, so we have to hardcode:
WAV_NAME = bge.logic.expandPath("//")+"Space_Reggae.wav"

# Actual work:
def amplitude(wav, t):
    head = int(t * wav.getframerate())
    delta = head - wav.tell()
    
    if delta < 0:
        delta = head - 0
        wav.rewind()
        
    chunk = array('h', wav.readframes(delta))
    lc = len(chunk)
    return (abs(sum(chunk) / lc)) if lc else 0 

def amp_z(cont):
    own = cont.owner
    
    act_snd = cont.actuators["Sound"]
    
    if not "init" in own:
        own["init"] = True
        own["wav"] = wave.open(WAV_NAME)
        own['x']=0
        cont.activate(act_snd)
    round = 8
    own['x'] = ((own['x'] * (round-1)) + (amplitude(own["wav"], act_snd.time) / 100))/round
    for obj in own.scene.objects:
        if 'init2' not in obj:
            obj['init2']=obj.worldPosition.copy()
        val = math.sin((obj.worldPosition.magnitude*2)+(own['x']*.66))
        #val = math.sin(obj.worldPosition[0])+math.sin(obj.worldPosition[1])+(own['x']*3.28) * .66
        obj.color = [val,val,val,1]
        obj.worldPosition = obj['init2']+Vector([0,0,val])
        
