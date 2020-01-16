//relies on jQuery being implemented on the html page
const adduser = function(e) {
	let project = e.target.parentElement;
	project.removeEventListener('click');
	let projid = project.id;
	let input = document.createElement("div");
	input.innerHTML = 'Username: <input type="text" id="user"><br><button class="btn btn-primary" id="add">Add User to Project</button>'
	project.appendChild(input);
	let button = document.getElementById("add");
	button.addEventListener('click', add);
}

const add = function(e) {
	let project = e.target.parentElement;
	let user = document.getElementById('user');
	$.ajax({

	});
}

const createproj = function(e) {
	$.ajax({
		method: 'GET',
		url: '/create',
		success: function(data) {
			let project = document.createElement('div')
			project.innerHTML = ''
			project.id = data['projid'];
			let button = document.getElementById('create');
			button.addEventListener('click', create);
		},
		error: function(err) {
		}
	});
}

const create = function(e) {
	let form = document.getElementById('form');
	form.innerHTML = '<form action="/create" method="post">Title:<input type="text" name="name"><br>Description:<br><textarea name="description"></textarea><br><button type="submit" class="btn btn-primary">Create</button></form>';
}

document.getElementById('create').addEventListener('click', create);
