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
      }
    };
  },
  computed: {
    formatTime() {
      const minutes = Math.floor(this.time / 60);
      const seconds = this.time % 60;
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    },
  },
  methods: {
    startTimer() {
      if (this.timer) return;
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
    pauseTimer() {
      clearInterval(this.timer);
      this.timer = null;
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
