window.onload = function(){
	// 获取轮播图li
	var lun = document.getElementById('lun');
	var lis = lun.children[0].children;

	// 获取轮播图的长度
	var len = lis.length;

	// 获取轮播图圆点的li
	var listCircle = document.getElementById('list-circle');
	var lists = listCircle.children[0].children;

	// 获取左右箭头的元素
	var left = document.getElementById('left');
	var right = document.getElementById('right');

	// 定义变量index,表示图片下标
	var index = 0;

	//定义变量 来接收setInterval 的标记
	var run;

	// 定义函数 用定时器写轮播
	function autoRun(){
		run = setInterval(function(){
			// 移除当前录播图及圆点上的class
			lis[index].removeAttribute('class');
			lists[index].removeAttribute('class');

			// 下标加一
			index++

			// 判断下标不能超过图片的长度
			if(index == len){
				index = 0;
			}
			// 显示后一个
			lis[index].setAttribute('class','active');
			lists[index].setAttribute('class','list-active');
		},2000)
	}

	// 调用定时器
	autoRun();

	// 鼠标以上轮播图 暂停播放
	lun.onmouseover = function(){
		clearInterval(run);
		left.style.display='block';
		right.style.display='block';
	}
	// 鼠标移开 轮播图 继续
	lun.onmouseout = function(){
		autoRun();
		left.style.display='none';
		right.style.display='none';
	}
	//点击右侧箭头按钮
	right.onclick = function(){
		// 移除当前的图片class 和圆点class
		lis[index].removeAttribute('class');
		lists[index].removeAttribute('class');

		// 索引 ++
		index++;

		// 判断如果右侧点击到最后一张图  让回到第一张
		if(index == len){
			index = 0
		}

		// 给下一个的图片和圆点加class
		lis[index].setAttribute('class','active');
		lists[index].setAttribute('class','list-active');
	}
	// 点击左侧箭头按钮
	left.onclick = function(){
		// 移除当前的图片class 和圆点class
		lis[index].removeAttribute('class');
		lists[index].removeAttribute('class');
		
		// 索引--
		index--

		// 判断如果左侧点击到第一张图  让其返回到最后一张
		if(index<0){
			index = len-1;
		}

		// 给上一个的图片和圆点加class
		lis[index].setAttribute('class','active');
		lists[index].setAttribute('class','list-active');
	}

	// 鼠标以上圆点切换图片，循环圆点
	for(var i=0;i<lists.length;i++){
		// 使用闭包实现移上当前的圆点
		lists[i].onmouseover = (function(i){
			return function(){
				// 移除上一个的图片和圆点class
				lis[index].removeAttribute('class');
				lists[index].removeAttribute('class');
				// 把当前移上的i 赋值给索引
				index = i;
				// 给当前索引的图片和圆点 加class
				lis[index].setAttribute('class','active');
				lists[index].setAttribute('class','list-active');
			}
		})(i)
	}
}