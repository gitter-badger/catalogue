function escapedots(str){
		return str.replace(/\./g, "\\.");
}

function Open_TypeWidget(controllerDOM){
	this.controllerDOM = controllerDOM;
	this.question_number = this.getQuestionNumber();
}
Open_TypeWidget.prototype = {
	getQuestionNumber : function(){
		var id = this.controllerDOM.attr("id");
		
		var question_numbers = id.split("_");
		if(question_numbers.length == 2)
			return question_numbers[1];
		return null;
	},
	getValue : function(){
		if(this.question_number == null)
			return null;

		var q = escapedots(this.question_number);

		return $("#question_"+q, this.controllerDOM).val();
	},
	setValue : function(value){
		if(this.question_number == null)
			return null;

		var q = escapedots(this.question_number);
		
		$("#question_"+q, this.controllerDOM).val(value);
	},	
	clear : function(){
		if(this.question_number == null)
			return null;

		var q = escapedots(this.question_number);
		
		$("#question_"+q, this.controllerDOM).val("");
	},
	hide : function(){
		this.controllerDOM.hide();
	},
	show : function(){
		this.controllerDOM.show();
	}		
}



function StackableWidget(questionNumber){
	this.widgets = [];
	this.answers = [];
	this.current_answer = null;
	this.question_number = questionNumber;
	this.valueField = $("#question_"+escapedots(this.question_number));

	var self = this;
	var qr = "div[id^=qc_"+questionNumber+".]";
	qr = escapedots(qr);

	//console.log(qr);
	$(qr).each(function(i,v){
		var widget = new Open_TypeWidget($(v));
  		self.widgets[widget.getQuestionNumber()] = widget;

  		widget.hide();
	});	

	this.bindControlls();
	this.cnt = 0;

	var value = this.valueField.val();
	//console.log("Value: "+value);
	if(value != undefined && value != ""){
		value = JSON.parse(value);
		
		for(x in value){
			var id = this.cnt++;			
			this.answers[id] = value[x];
			this.renderQuestion(id);
		}	
	}
	this.selectQuestion(0);

}
StackableWidget.prototype = {
	bindControlls : function(){
		var qn_dotfree = escapedots(this.question_number);
		var self = this;

		//console.log($("#stackable_newlinebtn_"+qn_dotfree));
		$("#stackable_newlinebtn_"+qn_dotfree).click( function(){
			self.newLineHandler();
		} );

		$("#stackable_save_"+qn_dotfree).click( function(){
			self.saveQuestion();
		} );
	},
	newLineHandler : function(){
		var qn_dotfree = escapedots(this.question_number);
		var self = this;

		var new_answer = {};
		
		var ans_id = self.cnt++;
	 	this.answers[ans_id] = new_answer;

	 	this.renderQuestion(ans_id);		
		this.selectQuestion(ans_id);
	},
	renderQuestion : function(qn){ 
		var self = this;

		//Render the question!!!
		var btn1 = $("<a href=\"#\"><img src=\"static/img/glyphicons_192_circle_remove.png\"></img></a>");
		btn1.click(function(e) {
			e.preventDefault();
			self.removeLine(qn);
			return false;
		});

		var btn2 = $("<a href=\"#\"><img src=\"static/img/glyphicons_150_edit.png\"></img></a>");
		btn2.click(function(e) {
			e.preventDefault();
			self.selectQuestion(qn);
			return false;
		});

		var snipet = this.createFormSnipet(qn);

		var td = $("<tr>").attr("id", "stackable_table_"+this.question_number+"_"+qn).append( [$("<td style=\"width: 90px;\">").append([btn2,"&nbsp;&nbsp;&nbsp;",btn1]), "<td snipet>"+snipet+"</td>"]);
		$("#stackable_table_"+escapedots(this.question_number)).append(td);		
	},
	removeLine : function(qn){
		var qn_dotfree = escapedots(this.question_number);
		var self = this;

		$("#stackable_table_"+qn_dotfree+"_"+qn).remove();
		delete this.answers[qn];

		this.refreshValue();

		this.deselectQuestion();
	},
	saveQuestion : function(){
		var answer = this.answers[this.current_answer];
		var qn_dotfree = escapedots(this.question_number);
		
		for( x in this.widgets){
			answer[this.widgets[x].getQuestionNumber()] = this.widgets[x].getValue();
		}

		var snipetText = this.createFormSnipet(this.current_answer);

		var tableRow = $("#stackable_table_"+qn_dotfree+"_"+this.current_answer)
		$("td[snipet]", tableRow).text(snipetText);
		this.refreshValue();
	},
	refreshValue : function(){
		var notNull = [];

		for( x in  this.answers){
			if( this.answers[x] != null )
				notNull.push(this.answers[x]);
		} 

		this.valueField.val( JSON.stringify(notNull) );	
	},
	selectQuestion : function(qn){
		var qn_dotfree = escapedots(this.question_number);
		var self = this;

		if(this.answers[qn] != undefined){

			if(this.current_answer != null){
				this.deselectQuestion();
			}

			$("#stackable_table_"+qn_dotfree+"_"+qn).addClass("info");
			this.current_answer = qn;
			var answer = this.answers[this.current_answer];

			for( x in this.widgets){
				this.widgets[x].setValue( answer[this.widgets[x].getQuestionNumber()] );

				this.widgets[x].show();
			}
		}
	},
	deselectQuestion : function(){
		var qn_dotfree = escapedots(this.question_number);
		var self = this;

		$("#stackable_table_"+qn_dotfree+"_"+this.current_answer).removeClass("info");
		//Clean All Controllers
		for( x in this.widgets){
			this.widgets[x].clear();

			this.widgets[x].hide();
		}
		this.current_answer = null;
	},
	createFormSnipet : function(qn){
		if(this.answers[qn] == undefined)
			return "";
		var n = 0;
		var snipet = "";
		for(x in this.answers[qn]){
			snipet = x +": "+ this.answers[qn][x]+"; "
			n++;
			if(n == 1) break;
		}

		return snipet;
	}
}