import dearpygui.dearpygui as dpg
import os
#import ctypes
# Include the following code before showing the viewport/calling `dearpygui.dearpygui.show_viewport`.
#ctypes.windll.shcore.SetProcessDpiAwareness(2)
class ChooseFontsPlugin():
	"""
	ChooseFontsPlugin adds the font menu item to your application that is using dearpygui as the GUI. Just insert the code 
 myFontsPlugin = EditFontsPlugin() in your dpg.menu_bar or dpg.viewport_menu_bar.

	This plugin enables you to change the global font style of your dearpygui application. If you don't have a Fonts folder, 
	the plugin will create one for you, as well as the files that will save the user's font preferences.
	"""
	def __init__(self):
		self.ignore = 'NO CUSTOM FONT, IGNORE'
		self.font_registry = dpg.add_font_registry()
		self.fontDict = dict()
		self.create_folders()
		self.create_font_library()
		self.create_font_window()
		self.create_font_menu()
	
	def create_folders(self):
		if not os.path.exists('Fonts'):
			os.mkdir('Fonts')
		if not os.path.exists('Fonts/USERFONT'):
			with open('Fonts/USERFONT', 'w') as f:
				f.write(self.ignore)
		if not os.path.exists('Fonts/USERSIZE'):
			with open('Fonts/USERSIZE', 'w') as f:
				f.write("16")
		if not os.path.exists('Fonts/USERSCALE'):
			with open('Fonts/USERSCALE', 'w') as f:
				f.write("1")


	def create_font_library(self):
		with open('Fonts/USERFONT', 'r') as f:
			self.userFont = f.read()
			if not self.userFont: self.userFont = self.ignore
		with open('Fonts/USERSIZE', 'r') as f:
			try: self.userSize = int(f.read())
			except: self.userSize = 16
			if not self.userSize: self.userSize = 16
		with open('Fonts/USERSCALE', 'r') as f:
			try: self.userScale = float(f.read())
			except: self.userScale = 1
			if not self.userScale: self.userScale = 1
		self.fontDict["YOUR FONTS"] = None
		for filename in os.listdir('Fonts'):
			if filename.endswith((".ttf","otf")):
				self.fontDict[filename] = f"Fonts/{filename}"
				# We add all of YOUR FONTS to the font registry so you can debug them using the font tool
				with dpg.font(self.fontDict[filename], 16, parent=self.font_registry) as f:
					dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
					dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
					dpg.add_font_chars([0x2013,0x2014,0x2015,0x2017,0x2018,0x2019,0x201A,0x201B,0x201C,0x201D,0x201E,0x2020,0x2021,0x2022,0x2026,0x2030,0x2032,0x2033,0x2039,0x203A,0x203C,0x203E,0x2044,0x204A])
					dpg.add_font_range(0x0, 0xF)
					dpg.add_font_range(0x00, 0xFF)
					dpg.add_font_range(0x000, 0xFFF)
					dpg.add_font_range(0x0000, 0xFFFF)
				dpg.bind_font(f)
		self.fontDict["WINDOWS FONTS"] = None
		try:
			for filename in os.listdir('C:\\Windows\\Fonts'):
				if filename.endswith((".ttf","otf")):
					self.fontDict[filename] = f"C:\\Windows\\Fonts\\{filename}"
		except:
			self.fontDict.pop("WINDOWS FONTS")
		if len(self.fontDict) > 0:
			if self.userFont in self.fontDict: 
				dpg.add_font(self.fontDict[self.userFont], size=self.userSize, parent=self.font_registry, tag="fntCFPNewFont")
				dpg.add_font_chars([0x2013,0x2014,0x2015,0x2017,0x2018,0x2019,0x201A,0x201B,0x201C,0x201D,0x201E,0x2020,0x2021,0x2022,0x2026,0x2030,0x2032,0x2033,0x2039,0x203A,0x203C,0x203E,0x2044,0x204A], parent="fntCFPNewFont")
				dpg.bind_font("fntCFPNewFont")


	def create_font_window(self):
		with dpg.window(label="Font Menu", width=400, height=400, show=False, tag="winCFPFontWindow", pos=(int(dpg.get_viewport_width()/2 - 200), int(dpg.get_viewport_height() / 2 - 200))):
			with dpg.child_window(autosize_x=True, height=-120):
				dpg.add_text("This is the font window. To use it, find your Fonts folder, and put in any .ttf or .otf font, and they will show up here.", wrap=0)
				dpg.add_text("Whatever font you choose will be applied to the whole application. Sometimes it's best to close and reopen the application after setting a font, in case things get weird.", wrap=0)
				dpg.add_combo(list(self.fontDict.keys()), label="Font Type", callback=lambda:self.build_fonts(), tag="cmbCFPFontType")
				dpg.add_input_int(label="Size", default_value=self.userSize, callback=lambda:self.build_fonts(), tag="intCFPSize")
				dpg.add_slider_float(default_value=self.userScale, label="Scale", callback=lambda:self.build_fonts(), tag="slideCFPFontScale", min_value=0.0, max_value=2.0, clamped=True)
				with dpg.group(horizontal=True):
					dpg.add_checkbox(label="Autosize?", tag="chkbxCFPAutosize", default_value=True)
					dpg.add_button(label="Change Font", callback=lambda: self.btnBuild())

			with dpg.child_window(autosize_x=True, height=100):
				dpg.add_text("the quick brown fox jumped over the lazy dog", wrap=0)
				dpg.add_text("THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG", wrap=0)
			with dpg.group(horizontal=True):
				dpg.add_button(label="Close", callback=lambda: dpg.configure_item("winCFPFontWindow", show=False))
				dpg.add_button(label="Save", callback=lambda: self.save_fonts())
				dpg.add_button(label="Reset to Default (Your Saves Won't Be Changed)", callback=lambda: dpg.bind_font("DEFAULT") and dpg.set_global_font_scale(1.0))

	def create_font_menu(self):
		self.font_menu = dpg.add_menu(label="Font")
		dpg.add_menu_item(label="Edit", callback=lambda: dpg.configure_item("winCFPFontWindow", show=True), parent=self.font_menu)
  
	def btnBuild(self):
		dpg.set_value("chkbxCFPAutosize", True)
		self.build_fonts()
		dpg.set_value("chkbxCFPAutosize", False)
  
	def build_fonts(self):
		if not dpg.get_value("chkbxCFPAutosize"): return
		self.userFont = dpg.get_value("cmbCFPFontType")
		self.userSize= dpg.get_value("intCFPSize")
		if self.userFont not in self.fontDict: return
		if not self.fontDict[self.userFont]: return
		try:
			if dpg.does_item_exist("fntCFPNewFont"): dpg.delete_item("fntCFPNewFont")
			newFont = dpg.add_font(self.fontDict[self.userFont], size=self.userSize, parent=self.font_registry, tag="fntCFPNewFont")
			dpg.add_font_range_hint(dpg.mvFontRangeHint_Default, parent="fntCFPNewFont")
			dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic, parent="fntCFPNewFont")
			dpg.add_font_chars([0x2013,0x2014,0x2015,0x2017,0x2018,0x2019,0x201A,0x201B,0x201C,0x201D,0x201E,0x2020,0x2021,0x2022,0x2026,0x2030,0x2032,0x2033,0x2039,0x203A,0x203C,0x203E,0x2044,0x204A], parent="fntCFPNewFont")
			dpg.add_font_range(0x0, 0xF, parent="fntCFPNewFont")
			dpg.add_font_range(0x00, 0xFF, parent="fntCFPNewFont")
			dpg.add_font_range(0x000, 0xFFF, parent="fntCFPNewFont")
			dpg.add_font_range(0x0000, 0xFFFF, parent="fntCFPNewFont")
			dpg.bind_font(newFont)
			self.userScale = float(dpg.get_value("slideCFPFontScale"))
			dpg.set_global_font_scale(self.userScale)
		except Exception as e:
			print(e)

	def save_fonts(self):
		with open('Fonts/USERFONT', 'w') as f:
			f.write(str(self.userFont))
		with open('Fonts/USERSIZE', 'w') as f:
			f.write(str(self.userSize))
		with open('Fonts/USERSCALE', 'w') as f:
			f.write(str(self.userScale))
		dpg.configure_item("winCFPFontWindow", show=False)

if __name__ == "__main__":
	dpg.create_context()
	dpg.create_viewport(title='Custom Title', width=1200, height=800)
	#from EditThemePlugin import EditThemePlugin
	dpg.show_debug()
	try:
		with dpg.window(tag="main2"):
			with dpg.child_window():
				dpg.add_text("This is text")
				dpg.add_button(tag="This is a button", label="THIS IS A BUTTON")
				dpg.add_checkbox(label="Check Box")
				with dpg.child_window(autosize_x=True, autosize_y=True):
					with dpg.tab_bar():
						with dpg.tab(label="THIS IS A TAB"):
							with dpg.tree_node(label="THIS IS A TREE NODE"):
								randListOfStuff = ['THIS', 'IS', 'A', 'LIST']
								dpg.add_combo(randListOfStuff)
								dpg.add_listbox(randListOfStuff)
		with dpg.viewport_menu_bar():
			with dpg.menu(label="Tools"):
				dpg.add_menu_item(label="Show About", 			callback=lambda:dpg.show_tool(dpg.mvTool_About))
				dpg.add_menu_item(label="Show Metrics", 		callback=lambda:dpg.show_tool(dpg.mvTool_Metrics))
				dpg.add_menu_item(label="Show Documentation", 	callback=lambda:dpg.show_tool(dpg.mvTool_Doc))
				dpg.add_menu_item(label="Show Debug", 			callback=lambda:dpg.show_tool(dpg.mvTool_Debug))
				dpg.add_menu_item(label="Show Style Editor", 	callback=lambda:dpg.show_tool(dpg.mvTool_Style))
				dpg.add_menu_item(label="Show Font Manager", 	callback=lambda:dpg.show_tool(dpg.mvTool_Font))
				dpg.add_menu_item(label="Show Item Registry", 	callback=lambda:dpg.show_tool(dpg.mvTool_ItemRegistry))
			#myEditTheme = EditThemePlugin()
			myFonts = ChooseFontsPlugin()
	except:
		pass
	dpg.set_primary_window("main2", True)
	dpg.setup_dearpygui()

	dpg.show_viewport()
	dpg.start_dearpygui()
	dpg.destroy_context()
