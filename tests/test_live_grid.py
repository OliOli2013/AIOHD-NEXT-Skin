import ast, importlib.util, tempfile, unittest, sys, types, subprocess, textwrap
from pathlib import Path
import xml.etree.ElementTree as E
ROOT=Path('root'); S=ROOT/'usr/share/enigma2/AIOHD'; P=ROOT/'usr/lib/enigma2/python/Plugins/Extensions/AIONextStyle'; C=ROOT/'usr/lib/enigma2/python/Components/Converter'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class LiveGridTests(unittest.TestCase):
 def test_syntax_and_panels(self):
  for p in ROOT.rglob('*.py'):ast.parse(p.read_text(),filename=str(p))
  trees=[E.parse(p) for p in S.rglob('*.xml')]; screens={s.get('name') for t in trees for s in t.getroot().findall('screen')}
  for t in trees:
   for e in t.getroot().iter('applet'):compile(textwrap.dedent(e.text or '').strip(), 'applet','exec')
   for e in t.getroot().iter('panel'):
    if e.get('name'):self.assertIn(e.get('name'),screens)
 def test_new_geometry(self):
  for f,n in [('skin_infobar.xml','InfoBar'),('skin_channelselection.xml','AIONextChannelLayout'),('skin_secondinfobar.xml','SecondInfoBar'),('skin_openatv.xml','Menu'),('skin_openatv.xml','EPGSelection'),('skin_openatv.xml','EventView'),('skin_movieplayer.xml','MoviePlayer')]:
   a=E.parse(S/'skinfiles'/f).getroot().find("screen[@name='%s']"%n)
   for e in a:
    if not e.get('position') or not e.get('size'):continue
    try:x,y=map(int,e.get('position').split(','));w,h=map(int,e.get('size').split(','))
    except ValueError:continue
    self.assertTrue(x>=0 and y>=0 and w>0 and h>0 and x+w<=1920 and y+h<=1080,(f,n,e.attrib))
 def test_epg_timeline(self):
  for f,n in [('skin_channelselection.xml','AIONextChannelLayout'),('skin_secondinfobar.xml','SecondInfoBar')]:
   a=E.parse(S/'skinfiles'/f).getroot().find("screen[@name='%s']"%n)
   self.assertEqual({e.text for e in a.findall("widget/convert[@type='AIONextEvent']")},{m+':'+str(i) for m in ['time','title'] for i in range(1,5)})
  a=E.parse(S/'skinfiles/skin_infobar.xml').getroot().find('screen');self.assertEqual(len(a.findall("widget/convert[@type='AIONextContext']")),1)
 def test_progress(self):
  a=ast.parse((C/'AIONextContext.py').read_text()); f=next(n for n in a.body if isinstance(n,ast.FunctionDef)); ns={};exec(compile(ast.Module(body=[f],type_ignores=[]),'test','exec'),ns);v=ns['event_percent'];self.assertEqual(v(100,60,130),50);self.assertEqual(v(100,60,100),0);self.assertIsNone(v(100,60,160));self.assertIsNone(v(100,0,100));self.assertIsNone(v(100,60,90))
 def test_profiles_and_palettes(self):
  t=load('live_grid_theme',P/'theme.py')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'skin.xml';p.write_bytes((S/'skin.xml').read_bytes());original=p.read_bytes()
   for mode in t.SURFACES:
    for key in t.PALETTES:
     t.apply_palette(str(p),key,mode);self.assertEqual(t.current_palette(str(p)),key);self.assertEqual(t.current_surface(str(p)),mode);self.assertFalse(t.apply_palette(str(p),key,mode))
   t.apply_palette(str(p),'aurora','studio');self.assertEqual(p.read_bytes(),original)
 def test_updater_security(self):
  u=load('live_grid_updater',P/'updater.py');url=u.DOWNLOAD_PREFIX+'4.0.1-r0/enigma2-plugin-skins-aiohd-next_4.0.1-r0_all.ipk';cmd=u.installer_command(url,'sha256:'+'a'*64)
  self.assertNotIn('--no-check-certificate',cmd);self.assertNotIn('_create_unverified_context',(P/'updater.py').read_text());self.assertIn('sha256sum -c',cmd);self.assertIn('mktemp -d',cmd);self.assertEqual(subprocess.run(['sh','-n','-c',cmd]).returncode,0)
  for bad in [url.replace('4.0.1-r0/','4.0.2-r0/'),url.replace('https://','http://'),url.replace('4.0.1-r0/','4.0.1-r0/extra/')]:
   with self.assertRaises(ValueError):u.installer_command(bad)
  u.installed_version=lambda:'4.0.0-r0';u._read_json=lambda **kw:{'tag_name':'4.0.1-r0','assets':[{'name':url.split('/')[-1],'browser_download_url':url,'digest':'sha256:'+'a'*64}]};self.assertEqual(u.fetch_latest()['digest'],'sha256:'+'a'*64)
 def test_dashboard_skin(self):
  a=ast.parse((P/'dashboard.py').read_text()); cls=next(n for n in a.body if isinstance(n,ast.ClassDef));skin=next(n.value.value for n in cls.body if isinstance(n,ast.Assign) and n.targets[0].id=='skin');r=E.fromstring(skin);self.assertEqual({e.get('name') for e in r.findall('widget')},{'clock','channel','event','next','signal','system','media','hint'})
if __name__=='__main__':unittest.main()
