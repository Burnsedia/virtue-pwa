// create a new task
<template>
  <div >
    <h1>Add Task</h1>   
    <input type="text" v-model="newTask" @click="addTask">
  </div>
</template>

<script>
export default {
  name: 'addTask' 
  date: () => {
    return {
      newTask: ''
    }
  },
  methods: {
   addTask() {
      if (this.newTask.trim().length == 0) {
        return
      }
      this.totask.push({
        id: this.idForTask,
        title: this.newTask,
        completed: false,
        editing: false,
        priority: 0
      })

      this.newTask = ''
      this.idForTask++
    },
}
</script>
