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
      this.$emit('add-task', this.newTask)
      this.newTask = ''
    }
  } 

}
</script>
