<template>
  <div class="his-box">
    <div class="hint">
      当前浏览功能区：<span v-if="type !== ''">{{ type }}</span><span v-else>全部</span><i
        style="margin-left: 8px; font-size: 20px"
        :class="{
          'iconfont icon-bianhuajiance': type === '变化检测',
          'iconfont icon-mubiaojiance': type === '目标检测',
          'iconfont icon-erfenleibianhuajiance16px': type === '地物分类',
          'iconfont icon-changjingguanli' : type === '场景分类',
          'iconfont icon-jishu' : type === '图像复原'
        }"
      />
    </div>
    <el-table
      ref="multipleTable"
      :data="tableData"
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" />
      <el-table-column label="日期">
        <template #default="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.create_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="功能区">
        <template #default="scope">
          <span id="bigtitle"><i
            style="font-size: 18px; margin-right: 6px"
            :class="{
              'iconfont icon-bianhuajiance': scope.row.type === '变化检测',
              'iconfont icon-mubiaojiance': scope.row.type === '目标检测',
              'iconfont icon-erfenleibianhuajiance16px':
                scope.row.type === '地物分类',
              'iconfont icon-changjingguanli' : scope.row.type === '场景分类',
              'iconfont icon-jishu' : scope.row.type ==='图像复原'
            }"
          />{{ scope.row.type }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="原图">
        <template #default="scope">
          <img
            :src="global.BASEURL + scope.row.before_img"
            min-width="70"
            height="70"
            class="goup"
            alt="原图"
            @click="previewOnePic(scope.row.before_img)"
          >

          <img
            v-if="scope.row.type === '变化检测'"
            :src="global.BASEURL + scope.row.before_img1"
            min-width="70"
            height="70"
            class="goup"
            style="margin-left: 20px"
            alt="原图"
            @click="previewOnePic(scope.row.before_img1)"
          >
        </template>
      </el-table-column>
      <el-table-column label="结果图/预测结果">
        <template #default="scope">
          <img
            v-show="scope.row.type !== '场景分类'"
            :src="global.BASEURL + scope.row.after_img"
            min-width="70"
            height="70"
            class="goup"
            alt="结果图"
            @click="previewOnePic(scope.row.after_img)"
          >
          <div v-show="scope.row.type === '场景分类'">
            {{ Object.keys(scope.row.data)[0] }}:
            {{ scope.row.data[(Object.keys(scope.row.data)[0])] }}
          </div>
        </template>
      </el-table-column>

      <el-table-column label="操作">
        <template #default="scope">
          <el-button
            size="default"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
          >
            删除
          </el-button>
          <el-button
            v-show="scope.row.type !== '变化检测'&&scope.row.type !=='场景分类'"
            size="default"
            type="primary"
            @click="previewTwoPic(scope.row.before_img, scope.row.after_img)"
          >
            预览
          </el-button>
          <el-button
            v-show="scope.row.type === '场景分类'"
            size="default"
            type="primary"
            @click="previewOnePic(scope.row.before_img, scope.row.after_img)"
          >
            预览
          </el-button>
          <el-button
            v-show="scope.row.type ==='变化检测'"
            size="default"
            type="primary"
            @click="
              previewThreePic(
                scope.row.before_img,
                scope.row.before_img1,
                scope.row.after_img
              )
            "
          >
            预览
          </el-button>
          <el-button
            v-show="scope.row.type !== '场景分类'"
            size="default"
            type="primary"
            @click="
              downloadimgWithWords(
                scope.row.id,
                global.BASEURL + scope.row.after_img,
                `${scope.row.type}结果图.png`
              )
            "
          >
            下载
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div
      type="primary"
      style="margin-left: 16px"
      class="fundrawer hidden-md-and-down"
      @click="fundrawer = true"
    >
      <div class="drawer2">
        <span style="color: red; font-family: Microsoft JhengHei UI, sans-serif">功能筛选</span>
      </div>
      <div class="drawer3">
        <i
          class="iconfont icon-shaixuan"
          style="color: red"
        />
      </div>
    </div>

    <el-drawer
      v-model="fundrawer"
      title="功能区筛选"
      :direction="direction"
      :size="size"
    >
      <el-menu
        class="el-menu-vertical-demo"
        text-color="black"
        background-color="white"
      >
        <el-menu-item-group>
          <el-menu-item
            index="1"
            @click="onlyDetectChanges"
          >
            <h3>
              <i class="iconfont icon-bianhuajiance" />变化检测
            </h3>
          </el-menu-item>
          <el-menu-item
            index="2"
            @click="onlyDetectTargets"
          >
            <h3>
              <i
                class="iconfont icon-mubiaojiance"
                style="font-size: 25px"
              />目标检测
            </h3>
          </el-menu-item>
          <el-menu-item
            index="3"
            @click="onlyClassify"
          >
            <h3>
              <i
                class="iconfont icon-erfenleibianhuajiance16px"
                style="font-size: 13px"
              />地物分类
            </h3>
          </el-menu-item>
          <el-menu-item
            index="4"
            @click="onlyClassifyScenes"
          >
            <h3>
              <i
                class="iconfont icon-changjingguanli"
                style="font-size: 22px"
              />场景分类
            </h3>
          </el-menu-item>
          <el-menu-item
            index="5"
            @click="onlyRestoreImgs"
          >
            <h3>
              <i
                class="iconfont icon-jishu"
                style="font-size: 22px"
              />图像复原
            </h3>
          </el-menu-item>
          <el-menu-item
            index="6"
            @click="goBackData"
          >
            <h3><i class="iconfont icon-fuyuan" />列表复原</h3>
          </el-menu-item>
        </el-menu-item-group>
      </el-menu>
    </el-drawer>
    <div
      v-show="tableData.length !== 0"
      style="margin-top: 20px"
    >
      <el-button @click="toggleSelection(tableData)">
        全选
      </el-button>
      <el-button @click="toggleSelection()">
        取消选择
      </el-button>
      <el-button
        type="danger"
        @click="deleteAll()"
      >
        删除
      </el-button>
      <el-button
        type="primary"
        @click="downLoadAll()"
      >
        下载
      </el-button>
    </div>
    <el-row justify="center">
      <el-col
        :xs="24"
        :sm="24"
        :md="10"
        :lg="11"
        :xl="10"
        style="margin-right: 40px"
      >
        <el-pagination
          background
          :page-size="pageSize"
          layout="prev, pager, next, jumper"
          :total="total"
          :current-page="currentPage"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          @next-click="goNextPage"
          @prev-click="goPrePage"
        />
      </el-col>
    </el-row>

    <el-dialog
      v-model="dialogVisible"
      :modal="false"
      title="图片预览"
      width="75%"
      fullscreen
      center
    >
      <div v-if="flag === 2">
        <el-row justify="space-evenly">
          <img
            id="pre-img"
            :src="previewPic1"
            alt="预览"
          >

          <img
            id="pre-img"
            :src="previewPic2"
            alt="预览"
          >
        </el-row>
      </div>
      <div v-else-if="flag === 1">
        <el-row justify="space-evenly">
          <img
            id="pre-img"
            :src="previewPic1"
            alt="预览"
          >
        </el-row>
      </div>
      <div v-else-if="flag === 3">
        <el-row justify="space-evenly">
          <img
            id="pre-img"
            :src="previewPic1"
            alt="预览"
          >

          <img
            id="pre-img"
            :src="previewPic3"
            alt="预览"
          >

          <img
            id="pre-img"
            :src="previewPic2"
            alt="预览"
          >
        </el-row>
        <el-row />
      </div>
      <el-row
        type="flex"
        justify="center"
      >
        <el-col :span="1">
          <el-button
            type="primary"
            @click="dialogVisible = false"
          >
            OK
          </el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import { showFullScreenLoading, hideFullScreenLoading } from "@/utils/loading";
import { historyGetPage, historyDelete } from "@/api/history";
import {
  previewOnePic,
  previewTwoPic,
  previewThreePic,
} from "@/utils/preview.js";
import { downloadimgWithWords } from "@/utils/download.js";

import global from "@/global.vue";
export default {
  name: "History",
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      document.querySelector(".el-main").scrollTop = 0;
    });
  },
  data() {
    return {
      delete: {
        ids: [],
      },
      type: "",
      fundrawer: false,
      direction: "rtl",
      size: "15%",
      pageSize: 10,
      total: 0,
      flag: "",
      currentPage: 1,
      multipleSelection: [],
      dialogVisible: false,
      previewPic1: "",
      previewPic2: "",
      previewPic3: "",
      tableData: [],
      global: {
        BASEURL: global.BASEURL,
      },
    };
  },
  mounted() {
    this.getTabelInfo();
  },
  methods: {
    previewOnePic,
    downloadimgWithWords,
    historyGetPage,
    historyDelete,
    previewTwoPic,
    previewThreePic,
    handleDelete(index, row) {
      this.$confirm("此操作将永久删除, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
          .then(() => {
            showFullScreenLoading(".his-box");
            this.delete.ids.push(row.id);
            this.historyDelete(this.delete).then((res) => {
              this.tableData.splice(index, 1);
              this.getTabelInfo();
              hideFullScreenLoading(".his-box");
              this.$message({
                type: "success",
                message: "删除成功!",
              });
            });
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "已取消删除",
            });
          });
    },
    deleteAll() {
      if (this.multipleSelection.length === 0) {
        this.$message.warning("请选择要删除的记录哦");
      } else {
        this.$confirm("此操作将永久删除, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
            .then(() => {
              showFullScreenLoading(".his-box");
              this.delete.ids = this.multipleSelection.map((item) => {
                return item.id;
              });

              this.historyDelete(this.delete).then((res) => {
                this.getTabelInfo();
                this.tableData = this.tableData.filter((item) => {
                  return this.multipleSelection.every((item2) => {
                    return item.id !== item2.id;
                  });
                });
                hideFullScreenLoading(".his-box");
                this.$message({
                  type: "success",
                  message: "删除成功!",
                });
              });
            })
            .catch(() => {
              this.$message({
                type: "info",
                message: "已取消删除",
              });
            });
      }
    },
    downLoadAll() {
      if (this.multipleSelection.length === 0) {
        this.$message.warning("请选择要下载的历史记录的图片哦");
      } else {
        for (let item of this.multipleSelection) {
          this.downloadimgWithWords(
              item.id,
              global.BASEURL + item.after_img,

              `${item.type}结果图.png`
          );
        }
      }
    },
    toggleSelection(rows) {
      if (rows) {
        rows.forEach((row) => {
          this.$refs.multipleTable.toggleRowSelection(row);
        });
      } else {
        this.$refs.multipleTable.clearSelection();
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleSizeChange(val) {
      this.pageSize = val;
      this.getTabelInfo();
    },
    handleCurrentChange(val) {
      this.page = val;
      this.currentPage = val;

      this.getTabelInfo();
    },
    getTabelInfo() {
      showFullScreenLoading(".his-box");

      this.historyGetPage(this.currentPage, 10, this.type).then((res) => {
        hideFullScreenLoading(".his-box");
        this.total = res.data.count;
        this.tableData = res.data.data;
      });
    },
    goNextPage() {
      this.getTabelInfo();
    },
    goPrePage() {
      this.getTabelInfo();
    },
    onlyDetectChanges() {
      this.type = "变化检测";
      this.getTabelInfo();
      this.fundrawer = false;
    },
    onlyDetectTargets() {
      this.type = "目标检测";
      this.getTabelInfo();
      this.fundrawer = false;
    },
    onlyClassify() {
      this.type = "地物分类";
      this.getTabelInfo();
      this.fundrawer = false;
    },
    onlyClassifyScenes() {
      this.type = "场景分类";
      this.getTabelInfo();
      this.fundrawer = false;
    },
    onlyRestoreImgs(){
      this.type = "图像复原";
      this.getTabelInfo();
      this.fundrawer = false;
    },
    goBackData() {
      this.type = "";
      this.getTabelInfo();
      this.fundrawer = false;
    },
  },
};
</script>

<style lang="less" scoped>
.his-box {
  min-height: 600px;
}
.hint {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
  "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji",
  "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  font-size: 18px;
  margin-bottom: 10px;
  margin-top: 10px;
}
.block {
  text-align: center;
  margin: 0 auto;
}
.el-pagination {
  text-align: center;
  margin: 20px 0 10px 0;
}
.dis {
  display: none;
}
#bigtitle {
  font-size: 16px;
}
#bigtitle:hover:after {
  left: 0%;
  right: 0%;
  width: 100%;
}
.fundrawer {
  position: fixed;
  z-index: 100;
  background: rgb(252, 252, 252);
  color: #000;
  top: 350px;
  right: 0;
  width: 34px;
  height: 120px;
  padding: 0.5rem;
  border-top-left-radius: 0.2rem;
  border-bottom-left-radius: 0.2rem;
  box-shadow: -5px 0 10px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.1s ease-in-out;
  cursor: pointer;
  font-family: SimHei sans-serif;
}
.drawer2 {
  font-size: 17px;
  font-weight: 1000;
  -webkit-writing-mode: vertical-rl;
  writing-mode: vertical-rl;
  color: rgb(92, 142, 228);
  background: rgb(237, 242, 245);
  padding: 0.12rem;
  border-radius: 0.2rem;
  height: 80px;
  text-align: center;
  width: 33px;
  span {
    display: block;
    padding-right: 6px;
  }
}
.drawer3 {
  width: 37px;
  text-align: center;
  margin-top: 6px;
  color: rgb(92, 142, 228);
  background: rgb(237, 242, 245);
  border-radius: 0.2rem;
  height: 30px;
  .iconfont {
    display: block;
    padding-top: 5px;
  }
}
.drawer2:hover,
.drawer3:hover {
  background-color: rgb(228, 235, 240);
}
.el-menu {
  width: 100%;
}
.is-active {
  color: white;
}
</style>