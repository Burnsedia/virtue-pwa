<template>
  <div class="card bg-base-100 shadow-xl p-6 mb-6">
    <h3 class="text-xl font-bold mb-4">Pomodoro Timer Settings</h3>
    <div class="form-control mb-4">
      <label class="label">
        <span class="label-text">Pomodoro Duration (minutes)</span>
      </label>
      <input type="number" v-model.number="pomodoroSettings.work" class="input input-bordered">
    </div>

    <div class="form-control mb-4">
      <label class="label">
        <span class="label-text">Short Break Duration (minutes)</span>
      </label>
      <input type="number" v-model.number="pomodoroSettings.shortBreak" class="input input-bordered">
    </div>

    <div class="form-control mb-4">
      <label class="label">
        <span class="label-text">Long Break Duration (minutes)</span>
      </label>
      <input type="number" v-model.number="pomodoroSettings.longBreak" class="input input-bordered">
    </div>

    <button @click="savePomodoroSettings" class="btn btn-primary">Save Pomodoro Settings</button>
  </div>

  <div class="card bg-base-100 shadow-xl p-6 mb-6">
    <h3 class="text-xl font-bold mb-4">Notification Preferences</h3>
    <div class="form-control">
      <label class="label cursor-pointer">
        <span class="label-text">Enable Sound Notifications</span>
        <input type="checkbox" v-model="notificationSettings.sound" class="toggle toggle-primary">
      </label>
    </div>
    <div class="form-control">
      <label class="label cursor-pointer">
        <span class="label-text">Enable Desktop Notifications</span>
        <input type="checkbox" v-model="notificationSettings.desktop" class="toggle toggle-primary">
      </label>
    </div>
    <button @click="saveNotificationSettings" class="btn btn-primary mt-4">Save Notification Settings</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pomodoroSettings: {
        work: 25,
        shortBreak: 5,
        longBreak: 15,
      },
      notificationSettings: {
        sound: true,
        desktop: false,
      },
    };
  },
  created() {
    this.loadSettings();
  },
  methods: {
    loadSettings() {
      // Load settings from localStorage or a user profile API
      const savedPomodoro = JSON.parse(localStorage.getItem('pomodoroSettings'));
      if (savedPomodoro) {
        this.pomodoroSettings = savedPomodoro;
      }
      const savedNotifications = JSON.parse(localStorage.getItem('notificationSettings'));
      if (savedNotifications) {
        this.notificationSettings = savedNotifications;
      }
    },
    savePomodoroSettings() {
      localStorage.setItem('pomodoroSettings', JSON.stringify(this.pomodoroSettings));
      alert('Pomodoro settings saved!');
    },
    saveNotificationSettings() {
      localStorage.setItem('notificationSettings', JSON.stringify(this.notificationSettings));
      alert('Notification settings saved!');
    },
  },
};
</script>
