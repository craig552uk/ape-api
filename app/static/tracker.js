(function(window, document, config, version){


    /***************************************************************
     * Polyfill Functions
     ***************************************************************/


    /**
     * Get elements by class name
     * For IE <9
     */
    if( !document.getElementsByClassName ){
        document.getElementsByClassName = function(id){
            var
            a = [],
            r = new RegExp('(^| )'+id+'( |$)'),
            e = document.getElementsByTagName("*"),
            i;
            for( i=0; i<e.length; i++ ){
                if( r.test(e[i].className) ){ a[i] = e[i]; }
            }
            return a;
        };
    }


    /***************************************************************
     * APE Functions
     ***************************************************************/


    var

    /*
     * Initialisation Function
     * @args: arguments object defined in page
     */
    init = function(args){

        // Get configuration from args or defaults
        config.version      = version;
        config.account_id   = args.account_id;
        config.timestamp    = args.ts.getTime() || (new Date()).getTime();
        config.debug        = args.debug        || false;
        config.class_prefix = args.class_prefix || "ape";
        config.cookie       = args.cookie       || "_ape_id";
        config.callback     = args.callback     || "_ape.callback";
        config.endpoint     = args.endpoint     || "beacon.js"

        if( config.debug ){ window._ape.config = config; }

        // Set callback handler in global scope;
        window._ape.callback = callback;

        // Build the request data payload
        payload = {
            cc: get_cookie(config.cookie),  // The APE cookie
            db: config.debug,               // Debug switch
            dl: window.location.href,       // Page URL
            dr: document.referrer,          // Referrer URL if set
            dt: document.title,             // Page title
            ev: 'pageload',                 // Page load event
            id: config.customer_id,         // The customer account ID
            ld: config.load,                // Page load time
            lg: window.navigator.language,  // Browser language
            pc: get_placeholder_classes(),  // The set of placeholder classes on this page
            px: config.class_prefix,        // Placeholder class prefix
            sc: window.screen.colorDepth,   // Screen colour depth
            sh: window.screen.height,       // Screen height
            sw: window.screen.width,        // Screen width
            ua: window.navigator.userAgent, // User Agent
            vr: config.version,             // Version number of this script
            jsonp: config.callback          // jsonp callback function
        };

        if( config.debug ){ window._ape.payload = payload; }

        // Send page load payload to beacon endpoint
        send_beacon(payload);
    },

    
    /*
     * Send a payload of data to the beacon end point
     * @payload: object of key-value pair data to send
     */
    send_beacon = function(payload){
        payload.rd = Math.random(); // To kick through agressive local caching
        add_script_tag(config.endpoint + '?' + url_serialize(payload));
    },


    /**
     * Callback handler for interactive jsonp requests
     * @payload: The json object in the response
     */
    callback = function(payload){
        console.log("Callback payload:")
        console.log(payload);
    },


    /* Add a script tag to the document
     * @url: The url of the script
     */
    add_script_tag = function(url){
        var
        elem = document.createElement('script'),
        node = document.getElementsByTagName('script')[0];
        elem.type = "text/javascript";
        elem.src = url;
        node.parentNode.insertBefore(elem, node);
    },


    /**
     * Return a string of all classes assigned to placeholders on the page
     */
    get_placeholder_classes = function(){
        var
        elements = document.getElementsByClassName(config.class_prefix),
        classes  = [];
        for( var i in elements ){
            classes.push(elements[i].className);
        }
        return classes.join(' ');
    },


    /**
     * Convert a flat object in to a URI encode string
     * @obj: Object of key-value pairs to URL encode
     */
    url_serialize = function(obj) {
        var str = [];
        for( var p in obj ){
            if( obj.hasOwnProperty(p) ){
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
            }
        }
        return str.join("&");
    },


    /**
     * Create a cookie
     * @name:  Name of the cookie
     * @value: Value of the cookie
     * @days:  Number of days until cookie expires (optional)
     */
    set_cookie = function(name, value, days){
        var expires = "";
        if( days ){
            var date = new Date();
            date.setTime(date.getTime() + (days*86400000));
            expires = "; expires=" + date.toGMTString();
        }
        document.cookie = name + "=" + value + expires + "; path=/";
    },


    /**
     * Get the value of a cookie
     * @name: The name of the cookie to get
     */
    get_cookie = function(name){
        name = name + '=';
        var cookies = document.cookie.split('; ');
        for( var i in cookies ) {
            cookie = cookies[i];
            if( cookie.indexOf(name) === 0 ){
                return cookie.substring(name.length, cookie.length);
            }
        }
        return '';
    };


    /***************************************************************
     * Get on with it
     ***************************************************************/


    // Do nothing if customer_id not provided
    if( window._ape.customer_id && window._ape.customer_id !== undefined ){
        init(window._ape);
    }


})(window, document, {}, "0.1");