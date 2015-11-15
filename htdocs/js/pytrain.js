var pytrain = function() {

	// number of railroad switches
	var NSWITCHES = 12;
	
    var svg = document.getElementById("railtrack_baselayout");
	
    var svgDoc = (svg.contentWindow || svg.contentDocument);
    if (svgDoc.document) svgDoc = svgDoc.document;
    
    var switches = [];
    
    var switchHandler = function(switchState) {
		
    	console.log("Received new state:",switchState);
		    
    	for (var i=0;i<NSWITCHES;++i) {
    		switches[i].toggle(switchState[i]);
    	}
	}
    var failHandler = function(err) {
    	console.error(err);
    }

    var Deferred = function() {
    	    	
    	this.then = function(successHandler,failHandler) {
    		
        	this.successHandler = successHandler;
        	this.failHandler = failHandler;

    	}
    	
    	this.resolve = function() {
    		
    		this.successHandler && this.successHandler.apply(this,arguments);
    	}

    	this.reject = function() {
    		
    		this.failHandler && this.failHandler.apply(this,arguments);
    	}
    };
    
    
    var xhr = function(args) {
    	
    	var url = args.url;
    	var method = args.method || 'GET';
    	
    	var d = new Deferred();
    		
    	var xmlhttp = new XMLHttpRequest();
   	
    	xmlhttp.onreadystatechange=function() {
    		if (xmlhttp.readyState==4) {
    			
    			if (xmlhttp.status==200) {
                                if (!xmlhttp.responseType && args.responseType == 'json' && typeof xmlhttp.response == 'string') {
                                    d.resolve(JSON.parse(xmlhttp.response));
                                }
                                else {
    				    d.resolve(xmlhttp.response);
                                }
    			}
    			else {
    				d.reject("HTTP query ["+method+" "+url+"] failed with code "+xmlhttp.status);
    			}
    		}
    	};
    	xmlhttp.open(method,url,true);
    	if (args.body) {
    		xmlhttp.send(body);
    	}
    	else {
    		xmlhttp.send();
    	}
        if (args.responseType) {
                xmlhttp.responseType = args.responseType;
        }
    	return d;
    };
    
    
    var fetchInitialState = function() {
        xhr({
    	    url:"/toggleSwitch",
		    method:"GET",
	        responseType:"json"
        }).then(switchHandler);
    };
	
    var define_switch = function(lbl) {
	   
    	var rwswitch = {
    			
    			link:  svgDoc.getElementById(lbl+"_link") || document.getElementById(lbl+"_link"),
    			node_0:  svgDoc.getElementById(lbl+"_0"),
    			node_1:  svgDoc.getElementById(lbl+"_1"),

    			state: 0,
    			
    			showState: function() {
    				this.node_0.style.display= this.state==0 ? "inline" : "none";
    				this.node_1.style.display= this.state!=0 ? "inline" : "none";
    			},
    			
    			toggle: function(newState) {
    				
    				if (this.state != newState) {
    					this.state = newState;
    					this.showState();
    				}
    			}
    	};
    	
        if (rwswitch.link) {
      	    rwswitch.link.addEventListener("mouseup",function() {
    		
    		    xhr({
    			    url:"/toggleSwitch?id="+lbl,
    			    method:"GET",
    			    responseType:"json"
    		    }).then(switchHandler);
     	    },false);
    	}

    	rwswitch.showState();
    	return rwswitch;
    } 
    
    for (var i=0;i<NSWITCHES;++i) {
    	
    	var lbl = "layer_switch_" + (i+1);
    	   	
        switches.push(define_switch(lbl));
    }
    

    // fetch initial state on startup
	fetchInitialState();
	
	setInterval(fetchInitialState,1000)
};
