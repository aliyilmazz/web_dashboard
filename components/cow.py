class cow:
    _attributes = {}
    def description(self):
        """
        description returns a string describing what component does.
        """
        return "Ceng On Web!"
    def getitem(self, index):
        """
        fetches the value from they key whose index is given as
        the second parameter.
        """
        return self._attributes[index]
    def setitem(self, index, value):
        """
        assigns given value to the corresponding key in the attribute
        dictionary regarding the given index.
        """
        self._attributes[index] = value
    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are used
        at design time to configure a components behaviour.
        """
        retlist = []
        for attr in self._attributes:
            retlist.append((attr,self._attributes[attr]))
        return retlist
    def methods(self):
        """
        methods return a list of method calls and their descriptions. The methods define the behaviour
        of the component at execution time. This way, application can interact with the components
        """
        methods_list = []
        for x in dir(self):
            if type(getattr(self, x)).__name__ == 'instancemethod':
                methods_list.append((x, getattr(self,x).__doc__))
        return methods_list
    def execute(self):
        """
        execute method will result in execution of component body. Result depends on the component
        type. A web application can generate HTML content where a graph based component gets
        all of inputs and generate outputs.
        execute is the basic behaviour of the component on execution time. The application is
        expected to call execute method of all added components to execute a design.
        """
        import sys
        import pickle
        import urllib
        import re

        response = urllib.request.urlopen('https://cow.ceng.metu.edu.tr/News/cowNews_left.php') # Make the request
        htmlString = response.read().decode('utf-8')
        threads = ["admin\.support", "announce", "announce\.admin", "an\.conference", "announce\.jobs", "an\.official", "announce\.sales", "an\.secondprog\.ceng", "an\.secondprog\.se"]
        massHTML = """
                <html>
        	    <head>
        		<meta charset="utf-8">
        		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        		<script>
        			$(document).ready(function(){
        				$("#button").click(function(){
                            var i = 0
                            $('input[type=checkbox]').each(function ()
                            {
                                var n = i.toString()
                                if (this.checked)
                                {
                                    $("#part"+n).show();
                                }
                                i=i+1;
                            });
                            $("#checks").hide();
        				});
        			});
        		</script>
                </head><body>
                """
        i=0
        for thread in threads:
                massHTML += "<div id='part" + str(i) + "' style='display: none;'>"
                arg = "(>" + thread + "<)(.+?)([0-9]+)(\D+?)(<\/small)"
                count = re.search(arg, htmlString, re.DOTALL)
                massHTML += thread.replace("\\","") + " (" + str(count.group(3)) + ")<br>"
                massHTML += "</div>"
                i+=1
        massHTML+="""
        <div id="checks"><input type="checkbox" id="0" name="admin\.support" value="on" > admin.support</input></br>
        <input type="checkbox" id="1" name="announce" value="on" > announce</input></br>
        <input type="checkbox" id="2" name="announce\.admin" value="on" /> announce.admin</input></br>
        <input type="checkbox" id="3" name="an\.conference" value="on" /> an.conference</input></br>
        <input type="checkbox" id="4" name="announce\.jobs" value="on" /> announce.jobs</input></br>
        <input type="checkbox" id="5" name="an\.official" value="on" /> an.official</input></br>
        <input type="checkbox" id="6" name="announce\.sales" value="on" /> announce.sales</input></br>
        <input type="checkbox" id="7" name="an\.secondprog\.ceng" value="on" /> an.secondprog.ceng</input></br>
        <input type="checkbox" id="8" name="an\.secondprog\.se" value="on" /> an.secondprog.se</input></br>
        <button id="button">Select</button>
        </div></body>"""
        return massHTML
