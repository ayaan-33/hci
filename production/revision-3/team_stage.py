import bpy,json,math,os,textwrap
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.display.render_aa='8';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.display.shading.show_specular_highlight=False;s.display.shading.background_type='WORLD';s.world.color=(.11,.13,.28);s.view_settings.view_transform='Standard'
regular=bpy.data.fonts.load('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');bold=bpy.data.fonts.load('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);return m
navy=mat('Cobalt ink',(.025,.055,.23));white=mat('Warm white',(.96,.98,1));mint=mat('Cyan',(.06,.95,.89));gold=mat('Amber',(1,.65,.045));purple=mat('Violet',(.51,.2,.92));pink=mat('Rose',(1,.1,.45));blue=mat('Blue',(.08,.36,.92));light=mat('Lilac stage',(.31,.34,.57));face=mat('Panel face',(.045,.14,.40));muted=mat('Soft label',(.60,.76,.91))
active=[]
def cube(n,p,sc,m,bevel=.06,dynamic=True):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.dimensions=sc;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if bevel:md=o.modifiers.new('Rounded depth','BEVEL');md.width=bevel;md.segments=3;o.modifiers.new('Normals','WEIGHTED_NORMAL')
 if dynamic:active.append(o)
 return o

def text(t,x,y,z,size=.35,m=white,width=45,isbold=False):
 bpy.ops.object.text_add(location=(x,y,z));o=bpy.context.object;o.data.body='\n'.join(textwrap.wrap(t,width=width));o.data.font=bold if isbold else regular;o.data.size=size;o.data.space_line=1.2;o.data.extrude=.004;o.data.bevel_depth=0;o.data.resolution_u=3;o.data.materials.append(m);active.append(o);return o
cube('Backdrop',(0,0,-1.1),(100,100,.3),light,dynamic=False)
# A genuine raised platform with coloured edge layers.
cube('Violet base',(0,0,-.5),(18,9.8,.6),purple,.2,False)
cube('Blue edge',(0,0,-.17),(17.8,9.6,.20),blue,.15,False)
cube('Main slide',(0,0,0),(17.5,9.3,.25),navy,.16,False)
for x,y,m in [(-10,3,pink),(9,5,gold),(10,-4,mint),(-10,-4,blue)]:
 o=cube('Sculpture',(x,y,-.1),(1,1,1),m,.15,False);o.rotation_euler=(.25,.3,.4)
bpy.ops.object.camera_add(location=(1.2,-3.5,19));cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=20.3;cam.rotation_euler=(math.radians(10),math.radians(2),0)
for section in json.load(open('/workspace/work/v2/slide_content.json')):
 if section['key']!='Immad-01':continue
 for j,(title,kicker,bullets) in enumerate(section['cards']):
  if title!='Meet teamGARI':continue
  for o in active:bpy.data.objects.remove(o,do_unlink=True)
  active=[];accent=[mint,gold,pink][j%3]
  text('teamGARI / C-10',-8,3.8,.15,.28,mint,50,True)
  text(section['speaker'],4.5,3.8,.15,.23,muted,30)
  cube('Header rule',(0,3.5,.27),(16,.025,.025),accent,.0)
  text('MEET TEAMGARI',-7.8,2.9,.15,.38,accent,42,True)
  
  text(section['chapter'].upper(),-7.8,-3.8,.15,.19,muted,50)
  if title=='Meet teamGARI':
   for n,name in enumerate(bullets):
    xx=-6+n*4;zz=.55
    cube('Member pedestal',(xx,-3.0,zz-.24),(3.5,.95,.35),[blue,purple,pink,blue][n],.12)
    text(name,xx-1.5,-3.0,zz,.29,white,17,True)
  else:
   for n,body in enumerate(bullets):
    yy=2.1-n*1.75;zz=.65+n*.1
    cube('Floating information card',(3.7,yy-.4,zz-.22),(8.6,1.65,.36),face,.12)
    cube('Raised accent',(-.48,yy-.4,zz),(.055,1.5,.07),accent,.015)
    text(f'{n+1:02d}',-.16,yy+.04,zz-.025,.21,accent,5,True)
    text(body,.45,yy+.06,zz-.025,.40,white,36)
  s.render.filepath='/workspace/work/v3/team-stage.png';bpy.ops.render.render(write_still=True)
  bpy.ops.wm.save_as_mainfile(filepath='/workspace/work/v3/team-stage.blend');raise SystemExit
for o in active:bpy.data.objects.remove(o,do_unlink=True)
active=[]
text('References & production',-7.8,3.5,.15,.52,white,65,True)
refs=['Soni et al. (2022) | doi:10.3389/fdgth.2022.954069','JMIR Human Factors (2021) | doi:10.2196/25787','Xiao et al. (2020) | doi:10.1145/3381804','Wei et al. | arXiv:2301.05843 (preprint reference)','Amershi et al. (2019) | Guidelines for Human-AI Interaction','W3C | WCAG 2.2 SC 4.1.3 and ARIA23','Typeform via tinycommand.com (2025) | vendor claim, not tested']
for i,line in enumerate(refs):text(line,-7.7,2.45-i*.65,.15,.29,white,105)
text('Original voices: Team C-10 / teamGARI',-7.7,-2.55,.15,.28,mint,90,True)
text('3D opening: synthetic AI narration. Editing and animation assisted by OpenAI Codex.',-7.7,-3.25,.15,.25,white,110)
s.render.filepath='/workspace/work/v2/slides/references.png';bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath='/workspace/work/v2/slide-stage.blend')
