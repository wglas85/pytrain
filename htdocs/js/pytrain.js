var pytrain = function() {

	// number of railroad switches
	var NSWITCHES = 9;
	
    var svg = document.getElementById("railtrack_baselayout");
	
    var svgDoc = (svg.contentWindow || svg.contentDocument);
    if (svgDoc.document) svgDoc = svgDoc.document;
    
    var switches = [];
    
    var define_switch = function(lbl) {
	   
    	var rwswitch = {
    			
    			link:  svgDoc.getElementById(lbl+"_link"),
    			node_0:  svgDoc.getElementById(lbl+"_0"),
    			node_1:  svgDoc.getElementById(lbl+"_1"),

    			state: 0,
    			
    			showState: function() {
    				this.node_0.style.display= this.state==0 ? "inline" : "none";
    				this.node_1.style.display= this.state!=0 ? "inline" : "none";
    			},
    			
    			toggle: function() {
    				this.state = this.state!=0 ? 0 : 1;
    				this.showState();
    			}
    	};
    	
    	rwswitch.link.addEventListener("mouseup",function() {
    		rwswitch.toggle();
    	},false);
    	
    	rwswitch.showState();
    	return rwswitch;
    } 
    
    for (var i=0;i<NSWITCHES;++i) {
    	
    	var lbl = "layer_switch_" + (i+1);
    	   	
        switches.push(define_switch(lbl));
    }
    
    
    
    
//	var layer_switch_1_0 = svgDoc.getElementById("layer_switch_1_0");
//	var layer_switch_2_1 = svgDoc.getElementById("layer_switch_2_1");

//	layer_switch_1_0.style.display="none";
//	layer_switch_2_1.style.display="none";

};
