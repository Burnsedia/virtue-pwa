<template>
  <div class="text-center">
    <div class="text-6xl font-bold">{{ formatTime }}</div>

    <div class="mt-4">
      <button @click="startTimer" class="btn btn-primary">Start</button>
      <button @click="pauseTimer" class="btn btn-secondary">Pause</button>
      <button @click="resetTimer" class="btn btn-accent">Reset</button>
    </div>

    <div class="mt-4">
      <button @click="setWorkSession" class="btn">Work</button>
      <button @click="setBreakSession" class="btn">Break</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      timer: null,
      time: 25 * 60, // Default to 25 minutes
      isWorkSession: true,
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
          if (this.isWorkSession) {
            this.setBreakSession();
          } else {
            this.setWorkSession();
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
      this.time = this.isWorkSession ? 25 * 60 : 5 * 60;
    },
    setWorkSession() {
      this.isWorkSession = true;
      this.time = 25 * 60;
      this.resetTimer();
    },
    setBreakSession() {
      this.isWorkSession = false;
      this.time = 5 * 60;
      this.resetTimer();
    },
    playSound() {
      const audio = new Audio('https://www.soundjay.com/buttons/sounds/button-1.mp3');
      audio.play();
    },
  },
};
</script>
