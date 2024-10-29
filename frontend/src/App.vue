<template>
  <div>
    <div class="tops">
      <h2>社工库查询📖</h2>
      <div class="Search">
        <input placeholder="请输入并按下回车进行搜索(忽略大小写)" type="text" class="searchInput" v-model="searchStr"
          v-on:keyup.enter="search" />
        <!-- <el-button size="large" :icon="Search">搜索</el-button> -->
      </div>
      <el-button class="upload-button1" type="success" @click="upload" plain>上传文件</el-button>

    </div>
    <div class="data-list">
      <h3>搜索结果</h3>
      <ul>
        <li v-for="(item, index) in results" :key="index" class="data-item">
          <p>{{ item }}</p>
        </li>
      </ul>
    </div>
  </div>
  <div class="upload-container">
    <el-drawer v-model="drawer" :with-header="false" class="custom-upload" title="文件上传" :direction="direction"
      :before-close="handleClose">
      <el-upload ref="upload" class="custom-upload" :limit="1" :on-exceed="handleExceed" :auto-upload="false"
        action="http://localhost:3010/upload" :file-list="fileList" :on-error="handleError" :on-change="handleChange">
        <!-- <template #trigger> -->
        <el-button type="primary" class="select-button">选择文件</el-button>
        <!-- </template> -->
        <el-button type="success" @click="submitUpload" class="upload-button">
          上传
        </el-button>
        <template #tip>
          <div class="upload-tip">
            一次只能上传一个文件
          </div>
        </template>

      </el-upload>



    </el-drawer>
  </div>

</template>

<script>
import axios from 'axios'
import { ElMessage } from 'element-plus';
import { handleError } from 'vue';
import { ref } from 'vue';
export default {
  setup() {
    const fileList = ref([])
    const upload = ref(null)
    const handleError = (err, file, fileList) => {
      console.log('上传失败:', err)
    }
    const submitUpload = () => {
      if (upload.value) {
        upload.value.submit();
      }
    }
    const handleChange = (file, fileList) => {
      // 上传完成后清空文件列表
      if (file.status === 'success' || file.status === 'fail') {
        fileList.length = 0;
      }
    };
    return {
      fileList,
      upload,
      handleError,
      submitUpload,
      handleChange,
    }

  },
  data() {
    return {
      searchStr: "",
      results: [],
      drawer: false,
      direction: "ttb",
    };
  },
  methods: {
    async search() {
      try {
        const response = await axios.get('http://localhost:3010/search', {
          params: {
            searchStr: this.searchStr
          }
        });
        console.log("response", response);
        this.results = response.data
        ElMessage.success("搜索成功")
      } catch {
        ElMessage.error("搜索失败")
      }
    },
    handleClose() {
      this.drawer = false;
    },
    upload() {
      this.drawer = true;
    }
  }
}
</script>
<style>
#main {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #fff;
  margin: 2em auto;
  width: 50em;
  border: 1px solid #ccc;
  padding: 1.5em;
  background: white;
}

.tops {
  position: relative;
  text-align: center;
  background-color: #27ae60;
  color: #fff;
  margin-bottom: 0;
  padding-bottom: 50px;
  padding-top: 20px;
  line-height: 20px;
  border-radius: 10px;
  /* 圆角 */
  margin-bottom: 20px;
}

h2 {
  font-size: 2em;
}

h1,
h2 {
  font-weight: normal;
}

h1 {
  color: #fff;
}

.searchInput {
  outline: none;
  height: 30px;
  width: 680px;
  border: 1px solid #ffffff;
  padding: 5px 30px 5px 30px;
  border-radius: 10px;
  font-size: 1em;
  font-family: BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial,
    sans-serif;
  margin-right: 10px;
}

.searchInput:focus {
  box-shadow: 2px 2px 2px #336633;
}

/* 整体容器 */
.data-list {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #e8f5e9;
  /* 淡绿色背景 */
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 标题 */
.data-list h3 {
  color: #2e7d32;
  /* 深绿色 */
  text-align: center;
  margin-bottom: 20px;
}

/* 列表样式 */
.data-list ul {
  list-style-type: none;
  padding: 0;
}

/* 列表项样式 */
.data-item {
  background-color: #a5d6a7;
  /* 列表项浅绿色背景 */
  color: #1b5e20;
  /* 字体深绿色 */
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  border: 1px solid #66bb6a;
  /* 边框颜色略深 */
  transition: transform 0.2s;
}

.data-item p {
  margin: 5px 0;
}

.data-item:hover {
  transform: translateY(-3px);
  /* 悬停时微微上升 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
  /* 悬停时添加阴影 */
}

/* 提示文本的样式 */
.upload-tip {
  font-weight: bold;
  margin-top: 10px;
}

.upload-button1 {
  margin-top: 25px;
  color: #ffffff;
}

.select-button {
  margin-right: 10px;
}

.upload-button {
  margin-right: 10px;
}

.upload-container {
  display: flex;
  align-items: center;
}
</style>
