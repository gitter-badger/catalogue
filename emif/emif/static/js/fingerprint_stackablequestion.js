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
	this.current_answer;
	
	this.my_widget;

	this.question_number = questionNumber;

	var self = this;
	var qr = "div[id^=qc_"+questionNumber+".]";
	qr = escapedots(qr);

	console.log(qr);
	$(qr).each(function(i,v){
		console.log(v);

		var widget = new Open_TypeWidget($(v));
  		self.widgets[widget.getQuestionNumber()] = widget;
		console.log(widget);

	});	

	this.bindControlls();
	this.cnt = 10;


}
StackableWidget.prototype = {
	bindControlls : function(){
		var qn_dotfree = escapedots(this.question_number);
		var self = this;

		console.log($("#stackable_newlinebtn_"+qn_dotfree));
		$("#stackable_newlinebtn_"+qn_dotfree).click( function(){
			self.newLineHandler();
		} );

		$("#stackable_save_"+qn_dotfree).click( function(){
			self.saveQuestion();
		} );
	},
	newLineHandler : function(){
		console.log(this);

		var qn_dotfree = escapedots(this.question_number);
		var self = this;

		var new_answer = {};
		
		var ans_id = self.cnt++;
	 	this.answers[ans_id] = new_answer;
		
		//Render the question!!!
		var btn1 = $("<button class=\"btn btn-mini\" type=\"button\">remove</button>");
		btn1.click(function() {
			self.removeLine(ans_id);
		});

		var btn2 = $("<button class=\"btn btn-mini\" type=\"button\">select</button>");
		btn2.click(function() {
			self.selectQuestion(ans_id);
		});


		var td = $("<tr>").attr("id", "stackable_table_"+self.question_number+"_"+ans_id).append( [$("<td>").append([btn1, btn2]), "<td>Nova</td>"]);
		$("#stackable_table_"+qn_dotfree).append(td);
		
		//$("#stackable_table_"+qn_dotfree).append("<tr id=\"stackable_table_"+self.question_number+"_"+ans_id+"\" class=\"success\"><td></td><td>Nova Pergunta</td></tr>");

		this.selectQuestion(ans_id);
	},
	removeLine : function(qn){
		var qn_dotfree = escapedots(this.question_number);
		var self = this;

		$("#stackable_table_"+qn_dotfree+"_"+qn).remove();
		delete this.answers[qn];
	},
	saveQuestion : function(){
		var answer = this.answers[this.current_answer];

		for( x in this.widgets){
			answer[this.widgets[x].getQuestionNumber()] = this.widgets[x].getValue();
		}

	},
	selectQuestion : function(qn){
		var qn_dotfree = escapedots(this.question_number);
		var self = this;

		if(this.answers[qn] != undefined){

			if(this.current_answer != null){
				this.deselectQuestion();
			}

			$("#stackable_table_"+qn_dotfree+"_"+qn).addClass("success");
			this.current_answer = qn;
			var answer = this.answers[this.current_answer];

			for( x in this.widgets){
				this.widgets[x].setValue( answer[this.widgets[x].getQuestionNumber()] );
			}
		}
	},
	deselectQuestion : function(){
		var qn_dotfree = escapedots(this.question_number);
		var self = this;

		$("#stackable_table_"+qn_dotfree+"_"+this.current_answer).removeClass("success");
		//Clean All Controllers
		for( x in this.widgets){
			this.widgets[x].clear();
		}
		this.current_answer = null;
	}
}