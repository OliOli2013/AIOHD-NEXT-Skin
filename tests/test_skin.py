import sys,types,importlib.util,unittest,math
from pathlib import Path
B=Path('root/usr/lib/enigma2/python')
def module(n,**kw):
 m=types.ModuleType(n);m.__dict__.update(kw);sys.modules[n]=m;return m
class Size:
 def __init__(self,w,h):self.w,self.h=w,h
 def width(self):return self.w
 def height(self):return self.h
class Widget:
 def __init__(self,parent=None):self.sz=Size(1280,620);self.pos=Size(0,0);self.text='';self.visible=True
 def size(self):return self.sz
 def resize(self,s):self.sz=s
 def move(self,p):self.pos=p
 def setFont(self,f):pass
 def setTransparent(self,v):pass
 def setText(self,v):self.text=v
class Label:
 def __init__(self,text=''):self.instance=Widget();self.setText(text)
 def setText(self,t):self.instance.text=t
 def getText(self):return self.instance.text
 def getSize(self):
  chars=max(1,self.instance.sz.w//17)
  return self.instance.sz.w,36*sum(max(1,math.ceil(len(s)/chars)) for s in self.getText().split('\n'))
 def hide(self):self.instance.visible=False
class StaticText:
 def __init__(self,text=''):self.text=text
 def setText(self,text):self.text=text
class Timer:
 def __init__(self):self.callback=[];self.timeout=types.SimpleNamespace(connect=lambda f:None)
 def start(self,*a):pass
 def stop(self):pass
class Action:
 def __init__(self,ctx,actions,prio):self.actions=actions
 def setEnabled(self,v):pass
class Converter:
 def __init__(self,arg):pass
class Poll:
 def __init__(self):pass
config=types.SimpleNamespace(osd=types.SimpleNamespace(language=types.SimpleNamespace(value='pl_PL')))
module('enigma',eSize=Size,ePoint=Size,eLabel=Widget,gFont=lambda *x:x,getDesktop=lambda n:types.SimpleNamespace(size=lambda:Size(1920,1080)),eEPGCache=object,eTimer=Timer)
for n in ['Components','Components.Converter','Components.Sources','Plugins','Plugins.Extensions']:module(n)
module('Components.Sources.StaticText',StaticText=StaticText)
module('Components.ActionMap',ActionMap=Action);module('Components.config',config=config)
module('Components.Converter.Converter',Converter=Converter);module('Components.Converter.Poll',Poll=Poll);module('Components.Element',cached=lambda f:f)
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
dialog=load('dialog',B/'Plugins/Extensions/AIONextStyle/dialog.py')
epg=load('next_epg',B/'Components/Converter/AIONextEvent.py')
class Screen(dict):
 def __init__(self,text,count):
  super().__init__();self.text=text;self.list=[('answer',i) for i in range(count)];self.instance=Widget();self['text']=Label(text);self['list']=Label();self['Title']=types.SimpleNamespace(master=types.SimpleNamespace(instance=Widget()))
class Tests(unittest.TestCase):
 def test_messages_fit_and_keep_all_text(self):
  for text in ['Zapisano.', 'Czy uruchomić ponownie interfejs?\nW czasie nagrywania wybierz Nie.', ('Błąd połączenia. Żółć / 東京\n'*200), 'X'*20000]:
   for count in [0,2,6,20]:
    s=Screen(text,count);dialog.layout_message(s)
    self.assertLessEqual(s.instance.sz.h,920);self.assertGreaterEqual(s.instance.pos.h,80)
    for key in ['text','list'] if count else ['text']:
     w=s[key].instance;self.assertLessEqual(w.pos.h+w.sz.h,s.instance.sz.h)
    if count:self.assertEqual(s['list'].instance.sz.h,min(count,6)*54)
    pages=[s['text'].getText()]
    if 'aioMessagePages' in s:
     while True:
      old=s._aio_message_page;s['aioMessagePages'].actions['right']()
      if s._aio_message_page==old:break
      self.assertLessEqual(s['text'].getSize()[1],s['text'].instance.sz.h);pages.append(s['text'].getText())
    self.assertEqual(''.join(pages),text);dialog.layout_message(s);self.assertEqual(s._aio_full_message,text)
 def test_future_events_without_current_and_single_query(self):
  epg._CACHE.clear()
  class Cache:
   calls=0
   def lookupEvent(self,q):
    self.calls+=1;return [(4,1400,60,'C'),(1,1100,60,'A'),(2,1200,60,'B'),(2,1200,60,'B'),(3,900,60,'old'),(5,1500,60,'D'),(6,1600,60,'E'),(8,None,None,'bad')]
  c=Cache()
  for offset in range(4):self.assertEqual(epg.upcoming(c,'selected-channel',1000)[offset][1],'ABCD'[offset])
  self.assertEqual(c.calls,1);self.assertEqual(epg.upcoming(c,'selected-channel',1210)[0][1],'C')
 def test_cache_bound_and_empty(self):
  epg._CACHE.clear();c=types.SimpleNamespace(lookupEvent=lambda q:[])
  for i in range(100):epg.upcoming(c,str(i),1000)
  self.assertLessEqual(len(epg._CACHE),32)
 def test_palette_atomic_and_reversible(self):
  import tempfile
  theme=load('theme',B/'Plugins/Extensions/AIONextStyle/theme.py')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'skin.xml';original=Path('root/usr/share/enigma2/AIOHD/skin.xml').read_bytes();p.write_bytes(original)
   for key in ['amber','violet','petrol','copper','jade','sakura','aurora']:
    self.assertTrue(theme.apply_palette(str(p),key));self.assertEqual(theme.current_palette(str(p)),key);self.assertFalse(theme.apply_palette(str(p),key))
   self.assertEqual(p.read_bytes(),original)
class FeatureTests(unittest.TestCase):
 def setUp(self):
  self.settings=types.SimpleNamespace(listSize=types.SimpleNamespace(value='large'),weatherEnabled=types.SimpleNamespace(value=True),weatherInline=types.SimpleNamespace(value=True),weatherProvider=types.SimpleNamespace(value='auto'),weatherPlugin=types.SimpleNamespace(value=''))
  module('aiofeatures.settings',settings=self.settings,tr=lambda pl,en:pl);package=module('aiofeatures');package.__path__=[]
 def test_channel_rows_and_no_global_change(self):
  channel=load('aiofeatures.channel',B/'Plugins/Extensions/AIONextStyle/channel.py')
  config.usage=types.SimpleNamespace(servicelist_twolines=types.SimpleNamespace(value=False))
  class Content:
   celServiceName=0;celServiceInfo=1;celServiceNumber=2
   def setItemHeight(self,h):self.height=h
   def setElementFont(self,k,f):pass
  class ServiceList:
   ServiceNameFontName='Next';listHeight=744;listWidth=1060;mode=1
   def __init__(self):self.l=Content();self.instance=Widget()
   def setItemsPerPage(self):self.l.setItemHeight(41)
   def setFontsize(self):self.ServiceNameFont=('Next',26)
   def setMode(self,mode):self.setItemsPerPage()
  for setting,rows,two in [('standard',18,False),('large',15,False),('xlarge',14,False),('standard',10,True),('large',9,True),('xlarge',8,True)]:
   config.usage.servicelist_twolines.value=two;self.settings.listSize.value=setting
   sl=ServiceList();channel.configure_channel_list({'list':sl})
   self.assertEqual(sl.ItemHeight,744//rows);self.assertLessEqual(sl.instance.sz.h,744)
   sl.setMode(1);self.assertEqual(sl.l.height,744//rows)
   sl.setFontsize();self.assertEqual(sl.ServiceNameFont,('NextBold',{'standard':32,'large':38,'xlarge':42}[setting]));self.assertEqual(sl.ServiceInfoFont,('Next',{'standard':26,'large':30,'xlarge':32}[setting]))
  untouched=ServiceList();untouched.setItemsPerPage();self.assertEqual(untouched.l.height,41)
 def test_weather_discovery_preference_and_missing_plugin(self):
  class Descriptor:
   WHERE_PLUGINMENU=1;WHERE_EXTENSIONSMENU=2;WHERE_MAINMENU=3
   def __init__(self,name,path,fnc):self.name=name;self.path=path;self.function=fnc
   def __call__(self,**kw):return self.function(**kw)
  calls=[];fn=lambda **kw:calls.append(kw)
  other=Descriptor('Foreca','/Extensions/Foreca',fn);preferred=Descriptor('WeatherPlugin','/Extensions/WeatherPlugin',fn)
  entries=[other,preferred,preferred,Descriptor('AIOHD NEXT — Weather','/AIONextStyle',fn),Descriptor('Media player','/Player',fn)]
  module('Components.PluginComponent',plugins=types.SimpleNamespace(getPlugins=lambda where:entries));module('Plugins.Plugin',PluginDescriptor=Descriptor)
  module('Screens');module('Screens.MessageBox',MessageBox=types.SimpleNamespace(TYPE_INFO=1,TYPE_ERROR=2))
  weather=load('aiofeatures.weather',B/'Plugins/Extensions/AIONextStyle/weather.py')
  discovered=weather.weather_plugins();self.assertEqual(len(discovered),2);self.assertIn('WeatherPlugin',weather.preferred_weather_key(discovered))
  self.assertEqual(len(weather.weather_plugins(show_all=True)),3)
  session=types.SimpleNamespace(open=lambda *a,**kw:calls.append(a));weather.open_weather(session,weather.preferred_weather_key(discovered));self.assertEqual(calls[-1],{'session':session})
  entries.clear();weather.open_weather(session,'missing|WeatherPlugin');self.assertIsInstance(calls[-1],tuple)
  weather_session=types.SimpleNamespace(screen={});weather.start_weather_sources(weather_session);self.assertEqual(weather_session.screen[weather.SOURCE_CITY].text,'Pogoda');self.assertIn('Ładowanie',weather_session.screen[weather.SOURCE_CONDITION].text)
 def test_updater_version_and_command_safety(self):
  updater=load('aiofeatures.updater',B/'Plugins/Extensions/AIONextStyle/updater.py')
  self.assertEqual(updater.CURRENT_PACKAGE_VERSION,'3.2.1-r5')
  self.assertTrue(updater.is_newer('3.2.1-r6'))
  self.assertTrue(updater.is_newer('3.2.2-r0'))
  self.assertFalse(updater.is_newer('3.2.1-r5'))
  self.assertFalse(updater.is_newer('3.2.1-r4'))
  url='https://github.com/OliOli2013/AIOHD-NEXT-Skin/releases/download/3.2.1-r6/enigma2-plugin-skins-aiohd-next_3.2.1-r6_all.ipk'
  cmd=updater.installer_command(url)
  self.assertIn('wget -q --no-check-certificate',cmd);self.assertIn('opkg install /tmp/aiohd-next-update.ipk',cmd)
  with self.assertRaises(ValueError):updater.installer_command('https://example.com/evil.ipk')
 def test_reported_openatv_screens_do_not_clip(self):
  import xml.etree.ElementTree as E
  root=Path('root/usr/share/enigma2/AIOHD/skinfiles')
  openatv=E.parse(root/'skin_openatv.xml').getroot()
  flash=openatv.find("screen[@name='FlashOnline']")
  self.assertIsNone(flash.find("panel[@name='T_Title']"))
  self.assertIsNotNone(flash.find("panel[@name='OPEN_SOURCE_INFO']"))
  self.assertIsNotNone(flash.find("widget[@source='description']"))
  shared=openatv.find("screen[@name='OPEN_SOURCE_INFO']")
  shared_title=shared.find("widget[@source='Title']")
  self.assertGreaterEqual(int(shared_title.get('size').split(',')[0]),1000)
  self.assertEqual(shared_title.get('noWrap'),'1')
  self.assertIsNotNone(shared.find('eLabel'))
  device=openatv.find("screen[@name='DeviceManager']")
  self.assertEqual(device.get('flags'),'wfNoBorder')
  software=openatv.find("screen[@name='SoftwareUpdate']")
  package_text=software.find("widget[@name='package_text']")
  self.assertEqual(package_text.get('noWrap'),'1')
  self.assertGreaterEqual(int(package_text.get('size').split(',')[0]),450)
  self.assertGreaterEqual(int(package_text.get('size').split(',')[1]),54)
  osd=openatv.find("screen[@name='OSDCalibration']")
  text=osd.find("widget[@source='text']");cfg=osd.find("widget[@name='config']")
  ty,th=map(int,(text.get('position').split(',')[1],text.get('size').split(',')[1]));cy=int(cfg.get('position').split(',')[1])
  self.assertGreaterEqual(th,220);self.assertGreaterEqual(cy,ty+th+20)
  infobar=E.parse(root/'skin_infobar.xml').getroot().find("screen[@name='InfoBar']")
  desc=next(w for w in infobar.findall('widget') if w.find("convert[@type='EventName']") is not None and (w.find("convert[@type='EventName']").text or '').strip()=='FullDescription')
  progress=next(w for w in infobar.findall('widget') if w.get('render')=='Progress' and w.find("convert[@type='EventTime']") is not None)
  dy,dh=map(int,(desc.get('position').split(',')[1],desc.get('size').split(',')[1]));py=int(progress.get('position').split(',')[1])
  self.assertGreaterEqual(py,dy+dh+8)
  plugin=(B/'Plugins/Extensions/AIONextStyle/plugin.py').read_text()
  self.assertIn("self['update_status']",plugin);self.assertIn('fetch_latest',plugin);self.assertIn('CURRENT_PACKAGE_VERSION',plugin)
 def test_bootlogo_backup_and_active_skin(self):
  import tempfile
  script=Path('control/postinst').read_text().split("<<'AIO_BOOTLOGO_PY'",1)[1].split('AIO_BOOTLOGO_PY',1)[0]
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);source=root/'usr/share/enigma2/AIOHD/bootlogo.mvi';source.parent.mkdir(parents=True);source.write_bytes(b'new-logo')
   settingsfile=root/'etc/enigma2/settings';settingsfile.parent.mkdir(parents=True);settingsfile.write_text('config.skin.primary_skin=Other/skin.xml')
   target=root/'usr/share/bootlogo.mvi';target.write_bytes(b'original-logo');code=compile(script.replace("Path('/", "Path('"+temp+"/"),'postinst-bootlogo','exec')
   exec(code,{});self.assertEqual(target.read_bytes(),b'original-logo');settingsfile.write_text('config.skin.primary_skin=AIOHD/skin.xml');exec(code,{})
   self.assertEqual(target.read_bytes(),b'new-logo');backup=root/'usr/share/bootlogo.mvi.before-aiohd-next';self.assertEqual(backup.read_bytes(),b'original-logo')
   source.write_bytes(b'newer-logo');exec(code,{});self.assertEqual(target.read_bytes(),b'newer-logo');self.assertEqual(backup.read_bytes(),b'original-logo')
 def test_xml_shared_layout_weather_and_contrast(self):
  import xml.etree.ElementTree as E
  root=Path('root/usr/share/enigma2/AIOHD');trees=[E.parse(p) for p in root.rglob('*.xml')];screens={s.get('name'):s for t in trees for s in t.getroot().findall('screen')}
  for t in trees:
   for p in t.getroot().iter('panel'):
    if p.get('name'):self.assertIn(p.get('name'),screens)
  s=screens['AIONextChannelLayout'];self.assertEqual(len(s.findall("widget/convert[@type='AIONextEvent']")),4);self.assertIsNotNone(s.find("widget[@render='Pig']"));self.assertIsNotNone(s.find('applet'))
  self.assertEqual(s.find("widget[@name='list']").get('backgroundColorSelected'),'nextSelection')
  weather_sources={w.get('source') for w in s.findall('widget') if (w.get('source') or '').startswith('session.AIONextWeather')};self.assertEqual(len(weather_sources),4)
  self.assertTrue(Path('root/usr/lib/enigma2/python/Components/Renderer/AIONextWeatherPixmap.py').is_file())
  openatv=E.parse(root/'skinfiles/skin_openatv.xml').getroot();info=openatv.find("screen[@name='information_common']/widget[@name='information']")
  self.assertIsNotNone(info);self.assertEqual(info.get('splitSeparated'),'1');self.assertGreaterEqual(int(info.get('colPosition')),380);self.assertGreaterEqual(int(info.get('splitMargin')),12)
  infobar=E.parse(root/'skinfiles/skin_infobar.xml').getroot().find("screen[@name='InfoBar']")
  self.assertIsNotNone(infobar)
  self.assertTrue(any((c.text or '').strip()=='FullDescription' for c in infobar.findall("widget/convert[@type='EventName']")))
  def luminance(v):
   c=[int(v[i:i+2],16)/255 for i in (3,5,7)];c=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in c];return sum(a*b for a,b in zip(c,[.2126,.7152,.0722]))
  theme=load('featuretheme',B/'Plugins/Extensions/AIONextStyle/theme.py')
  self.assertEqual(set(theme.PALETTES),set(k for k,_ in theme.PALETTE_CHOICES))
  self.assertTrue({'petrol','copper','jade','sakura'}.issubset(theme.PALETTES))
  for col in theme.STRONG_SELECTIONS.values():self.assertGreater(1.05/(luminance(col)+.05),4.5)
if __name__=='__main__':unittest.main(verbosity=2)
