module.exports = {
  data() {
    return {}
  },
  computed: {
    index() {
      return this.$store.state.index;
    },
    skin() {
      return this.$store.state.index.skins[this.$store.state.config.skinIndex];
    },
    maps() {
      return this.$store.state.maps;
    }
  },
  methods: {
    describeSolution(answer) {
      //描述答案
      if (answer) return `最佳答案${answer.length}步`
      else return '等你解决'
    },
    copyText(text) {
      let textarea = document.createElement("textarea"); //创建input对象
      let currentFocus = document.activeElement; //当前获得焦点的元素
      let toolBoxwrap = document.querySelector(".body"); //将文本框插入到NewsToolBox这个之后
      toolBoxwrap.appendChild(textarea); //添加元素
      textarea.value = text;
      textarea.focus();
      if (textarea.setSelectionRange) {
        textarea.setSelectionRange(0, textarea.value.length); //获取光标起始位置到结束位置
      } else {
        textarea.select();
      }
      let flag = document.execCommand("copy"); //执行复制
      toolBoxwrap.removeChild(textarea); //删除元素
      currentFocus.focus();
      return flag;
    }
  }
}
