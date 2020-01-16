//relies on jQuery being implemented on the html page
const edit = function(e) {
	console.log(e);
	let projid = document.getElementById('projid').value;
	let task = e;
	let id = e.id;
	let dataString = `id=${id}&projid=${projid}`;
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
	let content = document.getElementById("content").value;
	let deadline = document.getElementById("deadline").value;
	$.ajax({
		type: 'POST',
		url: '/edittask',
		data: `projid=${projid}&id=${id}&content=${content}&deadline=${deadline}`,
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
	let user = document.getElementById("username").value;
	let deleted = document.getElementById('temp');
	deleted.parentNode.removeChild(deleted);
	let dataString = `projid=${projid}&user=${user}`;
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

const create = function() {
	let assignment = document.createElement("div");
	assignment.id = 'temp';
	assignment.innerHTML = 'Assignee: <input type="text" id="username"><button class="btn btn-secondary" id="add">Assign</button>';
	document.getElementById("tasks").appendChild(assignment);
	let submit = document.getElementById('add');
	submit.addEventListener('click', newtask);
};

var tasks = document.getElementsByClassName("task");
for(var i = 0; i < tasks.length; i++) {
	tasks[i].addEventListener("click", edittask);
}
document.getElementById("create").addEventListener("click", create);
