import tornado.web
import tornado.template

class MyWebHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.loader = tornado.template.Loader("")

    def output( self, template, page_data ) :
        page_data[ 'loader' ] = self.loader
        output = self.loader.load( 'src/client/public/' + template + ".html").generate(page_data=page_data)
        self.write(output)

class MainHandler(MyWebHandler):

    def initialize(self):
        self.loader = tornado.template.Loader("")

    def get( self ) :
        self.output("index",{})
