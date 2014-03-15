"""An XBlock providing adaptive search."""

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment
import pkg_resources

import logging
log = logging.getLogger(__name__)


class AdSearchBlock(XBlock):
    """
    An XBlock which provides a search block. The instructor can add a prefix to the query and the last query 
    by any student is shown as suggestion..
    """

    query = String(help="Query string containing the last query", default='', scope=Scope.user_state_summary)
    prefix = String(help="Prefix for querys", default='', scope=Scope.settings)

    def student_view(self, context=None):  # pylint: disable=W0613
        """
        Create a fragment used to display the XBlock to a student.
        `context` is a dictionary used to configure the display (unused)

        Returns a `Fragment` object specifying the HTML, CSS, and JavaScript
        to display.
        """

        # Load the HTML fragment from within the package and fill in the template
        html_str = pkg_resources.resource_string(__name__, "static/html/adsearch.html")
        frag = Fragment(unicode(html_str).format(self=self))

        # Load the CSS and JavaScript fragments from within the package
        css_str = pkg_resources.resource_string(__name__, "static/css/adsearch.css")
        frag.add_css(unicode(css_str))

        js_str = pkg_resources.resource_string(__name__,
                                               "static/js/src/adsearch.js")
        frag.add_javascript(unicode(js_str))

        frag.initialize_js('AdSearchBlock')
        return frag

    problem_view = student_view

    @XBlock.json_handler
    def search(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Saves the last query from a user.
        """

        self.query = data['query']
        return {'query': self.prefix + self.query}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("Adaptive Search",
             """\
                <vertical_demo>
                    <adsearch/>
                    <adsearch prefix="edx " />
                </vertical_demo>
             """)
        ]
