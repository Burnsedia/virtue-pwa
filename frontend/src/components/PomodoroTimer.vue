<template>
  <div class="text-center">
    <div class="text-6xl font-bold">{{ formatTime }}</div>

    <div class="mt-4">
      <button @click="startTimer" class="btn btn-primary">Start</button>
      <button @click="pauseTimer" class="btn btn-secondary">Pause</button>
      <button @click="resetTimer" class="btn btn-accent">Reset</button>
    </div>

    <div class="mt-4">
      <button @click="setSession('work')" :class="{ 'btn-active': sessionType === 'work' }" class="btn">Pomodoro</button>
      <button @click="setSession('shortBreak')" :class="{ 'btn-active': sessionType === 'shortBreak' }" class="btn">Short Break</button>
      <button @click="setSession('longBreak')" :class="{ 'btn-active': sessionType === 'longBreak' }" class="btn">Long Break</button>
    </div>

    <div class="mt-8">
      <select v-model="selectedProject" @change="fetchIssues" class="select select-bordered w-full max-w-xs">
        <option disabled value="">Select a project</option>
        <option v-for="project in projects" :key="project.id" :value="project.id">{{ project.name }}</option>
      </select>
      <select v-model="selectedIssue" class="select select-bordered w-full max-w-xs">
        <option disabled value="">Select an issue</option>
        <option v-for="issue in issues" :key="issue.id" :value="issue.id">{{ issue.title }}</option>
      </select>
    </div>

    <div class="mt-8">
      <button @click="showSettings = true" class="btn btn-ghost">Settings</button>
    </div>

    <div v-if="showSettings" class="modal modal-open">
      <div class="modal-box">
        <h3 class="font-bold text-lg">Settings</h3>
        
        <div class="form-control">
          <label class="label">
            <span class="label-text">Pomodoro Duration (minutes)</span>
          </label>
          <input type="number" v-model.number="settings.work" class="input input-bordered">
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">Short Break Duration (minutes)</span>
          </label>
          <input type="number" v-model.number="settings.shortBreak" class="input input-bordered">
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">Long Break Duration (minutes)</span>
          </label>
          <input type="number" v-model.number="settings.longBreak" class="input input-bordered">
        </div>

        <div class="modal-action">
          <button @click="showSettings = false" class="btn">Close</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      timer: null,
      time: 25 * 60, 
      sessionType: 'work', // work, shortBreak, longBreak
      pomodoros: 0,
      showSettings: false,
      settings: {
        work: 25,
        shortBreak: 5,
        longBreak: 15,
      },
      projects: [],
      issues: [],
      selectedProject: '',
      selectedIssue: '',
      activeTimeLog: null,
    };
  },
  computed: {
    formatTime() {
      const minutes = Math.floor(this.time / 60);
      const seconds = this.time % 60;
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    },
  },
  created() {},
  mounted() {
    this.fetchProjects();
    this.fetchIssues();
  },
  watch: {
    selectedProject() {
      this.fetchIssues();
    }
  },
  methods: {
    async fetchProjects() {
      const res = await fetch('http://localhost:8000/api/projects/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      this.projects = await res.json();
    },
    async fetchIssues() {
      if (!this.selectedProject) return;
      const res = await fetch(`http://localhost:8000/api/issues/?project=${this.selectedProject}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      this.issues = await res.json();
    },
    async startTimer() {
      if (this.timer) return;
      if (this.sessionType === 'work' && !this.selectedIssue) {
        alert('Please select an issue to work on.');
        return;
      }

      if (this.sessionType === 'work') {
        const res = await fetch('http://localhost:8000/api/timelogs/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({
            issue: this.selectedIssue,
            start_time: new Date().toISOString(),
          }),
        });
        this.activeTimeLog = await res.json();
      }

      this.timer = setInterval(() => {
        if (this.time > 0) {
          this.time--;
        } else {
          this.pauseTimer();
          this.playSound();
          if (this.sessionType === 'work') {
            this.pomodoros++;
            if (this.pomodoros % 4 === 0) {
              this.setSession('longBreak');
            } else {
              this.setSession('shortBreak');
            }
          } else {
            this.setSession('work');
          }
        }
      }, 1000);
    },
    async pauseTimer() {
      clearInterval(this.timer);
      this.timer = null;

      if (this.activeTimeLog) {
        await fetch(`http://localhost:8000/api/timelogs/${this.activeTimeLog.id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({
            end_time: new Date().toISOString(),
          }),
        });
        this.activeTimeLog = null;
      }
    },
    resetTimer() {
      this.pauseTimer();
      this.time = this.settings[this.sessionType] * 60;
    },
    setSession(type) {
      this.sessionType = type;
      this.resetTimer();
    },
    playSound() {
      const audio = new Audio('https://www.soundjay.com/buttons/sounds/button-1.mp3');
      audio.play();
    },
  },
};
</script>
