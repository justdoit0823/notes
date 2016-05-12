
var page = require('webpage').create();
var system = require('system');

page.onConsoleMessage = function(msg) {
    console.log(msg);
};

if(system.args.length == 1){
    console.log('usage: jobs_at_v2ex.js url');
    phantom.exit();
}


var url = system.args[1];


var get_job_list = function(status) {
    if(status === "success") {
	page.evaluate(function() {
	    job_item_list = document.getElementsByClassName('item_title');
	    item_len = job_item_list.length;
	    for(var i = 0; i < item_len; i++){
		spanItem = job_item_list[i].firstChild;
		console.log(spanItem.innerHTML + ' ' + spanItem.href);
	    }
	});
    }
    phantom.exit();
};


page.open(url, get_job_list);
