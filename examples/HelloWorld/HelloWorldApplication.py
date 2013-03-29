# HelloWorldApplication.py
# (C)2013
# Scott Ernst

from pyglass.app.PyGlassApplication import PyGlassApplication

#___________________________________________________________________________________________________ HelloWorldApplication
class HelloWorldApplication(PyGlassApplication):

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: debugRootResourcePath
    @property
    def debugRootResourcePath(self):
        return ['resources']

#___________________________________________________________________________________________________ GS: splashScreenUrl
    @property
    def splashScreenUrl(self):
        return None

#___________________________________________________________________________________________________ GS: appGroupID
    @property
    def appGroupID(self):
        return 'pyglass_examples'

#___________________________________________________________________________________________________ GS: mainWindowClass
    @property
    def mainWindowClass(self):
        from HelloWorldMainWindow import HelloWorldMainWindow
        return HelloWorldMainWindow

####################################################################################################
####################################################################################################

if __name__ == '__main__':
    HelloWorldApplication().run()
