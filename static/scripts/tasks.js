//relies on jQuery being implemented on the html page
const edit = function(e) {
	console.log(e);
	let task = e;
	let id = e.id;
	let dataString = `id=${id}`;
	console.log(dataString);
	$.ajax({
		type: 'GET',
		url: '/edittask',
		data: dataString,
		success: function(html) {
			task.removeEventListener("click", edittask);
			console.log(task.innerHTML);
			task.innerHTML = html;
			console.log('changed html');
			document.getElementById("push").addEventListener("click", pushedits);
		},
		error: function(error) {
			console.log('could not edit task:');
			console.log(error);
			//alert(error);
		}
	});
};

const edittask = function(e) {
	edit(e.target);
}

const pushedits = function(e) {
	let projid = document.getElementById("projid").value;
	let id = document.getElementById("id").value;
	let stat = document.getElementById("status").value;
	let content = document.getElementById("content").value;
	let deadline = document.getElementById("deadline").value;
	let user = document.getElementById("user").value;
	$.ajax({
		type: 'POST',
		url: '/edittask',
		data: `projid=${projid}&id=${id}&stat=${stat}&content=${content}&deadline=${deadline}&user=${user}`,
		success: function(html) {
			let task = document.getElementById(`${id}`);
			task.innerHTML = html;
			task.addEventListener("click", edittask);
		},
		error: function() {
			console.log('could not push edits');
		}
	});
};

const newtask = function(e) {
	let projid = document.getElementById("projid").value;
	let dataString = `projid=${projid}`;
	console.log(dataString)
	$.ajax({
		type: 'POST',
		url: '/newtask',
		data: dataString,
		dataType: "JSON",
		success: function(data) {
			console.log(data['id']);
			let task = document.createElement('div');
			console.log(task.id);
			document.getElementById("tasks").appendChild(task);
			task.id = `${data['id']}`;
			console.log(task);
			edit(task);
		},
		error: function(error) {
			console.log('could not create new element');
			console.log(error);
			//alert(error);
		}
	});
};

var tasks = document.getElementsByClassName("task");
for(var i = 0; i < tasks.length; i++) {
	tasks[i].addEventListener("click", edittask);
}
document.getElementById("create").addEventListener("click", newtask);
