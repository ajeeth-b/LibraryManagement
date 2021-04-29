var table = document.getElementById('data-table');
var page_no = 1;
var row_per_page = 2;
var table_data = {};
var data_count = 0;
var has_all_data = false;

function update_table_rows(start, end){
	while(table.rows.length > 1){
		table.deleteRow(1);
	}

	for(;start<=end; start++){
		data = table_data['d'+start];
		if (data != undefined){
			row = table.insertRow(-1);
			row.insertCell(0).innerHTML = data.isbn;
			row.insertCell(0).innerHTML = data.author;
			row.insertCell(0).innerHTML = data.name;
			row.insertCell(3).innerHTML =  "<a href='#' onclick=borrow_book("+ data.id  + ",'" + 'd'+start +"')>Take</a>"
		}
	}
	update_pagination();
}

function update_table(callback=false){
	start = (page_no-1)*row_per_page+1;
	end = (page_no)*row_per_page;

	start_data = table_data['d'+start]
	if ((start_data == undefined) && (callback != true)){
		update_local_db(start-1, true);
	}else{
		update_table_rows(start, end);
	}
}

update_table();

function on_new_page(new_page_no){
	page_no = new_page_no;
	update_table();
}

function update_pagination(){
	paginate_count = Math.ceil(data_count/row_per_page);
	paginate = document.getElementById('pagination');
	html_content = ''
	for(i = 1; i<=paginate_count; i++){
		html_content += "<a href='#' onclick='on_new_page("+i+")'>"+i+"</a>"
	}
	if (has_all_data == false){
		html_content += "<a href='#' onclick='on_new_page("+i+")'>next</a>"
	}
	paginate.innerHTML = html_content;
}


function add_data_to_table_data(data){
	for(i = 0; i < data.books.length; i++){
		if (table_data['d'+(i+data.prev_offset+1)] == undefined){
			table_data['d'+(i+data.prev_offset+1)] = data.books[i];
			data_count++;
		}
	}

	if (data.has_more ==  false){
		has_all_data = true;
	}
}

function update_local_db(offset, update_table_later=false){
	
	url = '/api/library/books?available=true&offset='+offset+'&per-page='+row_per_page;

	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function(){
		if (this.readyState == 4){
			if (this.status == 200){
				add_data_to_table_data(JSON.parse(xhr.responseText));
				if (update_table_later == true){
					update_table(callback=true);
				}
			}else{
				console.log('Error', this.status)
			}
		}
	}

	xhr.open("GET", url);
	xhr.send();
}



function borrow_book(book_id, data_id){
	url = '/api/library';

	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function(){
		if (this.readyState == 4){
			if (this.status == 200){
				borrow_book_handler(JSON.parse(xhr.responseText), data_id);
			}else{
				console.log('Error', this.status)
			}
		}
	}

	xhr.open("POST", url);
	xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	xhr.send(JSON.stringify({ "book_id":book_id, "member_id":member_id }));
}

function borrow_book_handler(response_data, data_id){
	document.getElementById('message').innerHTML = response_data.message;

	console.log(table_data);
	delete table_data[data_id];
	data_count--;
	update_table();
	setTimeout(
		function(){
			window.location.reload();
		},
		1000);
}
