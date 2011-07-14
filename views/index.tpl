%include header title = title
<div class="box">
	%if len(flush_message['success']) >= 0:
		<div class="box success">{{flush_message['success']}}</div>
	%end
	
	%if len(flush_message['error']) >= 0:
		<div class="box error">{{flush_message['error']}}</div>
	%end

	<div class="box todos">
		<h2 class="box">待辦事項</h2>
		<ul>
			%for todo in todos:
			<li >
				%if todo.status is False:
					{{todo.topic}}
				%else:
					<del>{{todo.topic}}</del>
				%end
				&nbsp;
				
				%if todo.status is False:
					<a href="/finish/{{todo.id}}">完成</a>,
				%else:
					<a href="/unfinish/{{todo.id}}">恢復</a>,
				%end
				<a href="/edit/{{todo.id}}">編輯</a>,
				<a href="/delete/{{todo.id}}" onclick="return confirm('刪除以後不能還原,你確定嗎?')">刪除</a>
			</li>
			%end
		</ul>
	</div>

	<div class="box post">
		<h2>新增</h2>
		<form action="/new" method="post" id="post_new">
			<p><input type="text" name="name" class="long_txt" /></p>
			<p><input type="submit" class="submit" value="添加" /></p>
		</form>
	</div>
</div>
%include footer title = title
