<template>
  <div>
    <table v-if="adrData.length > 0">
      <thead v-if="headerRow">
        <tr>
          <th>Title</th>
          <th>Status</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(adr, index) in displayAdrData" :key="index">
          <td>
            <a v-if="links" :href="adr.url" target="_blank">{{ adr.title }}</a>
            <span v-else>{{ adr.title }}</span>
          </td>
          <td style="text-align: center;" :class="getRowClass(adr.status)">{{ adr.status }}</td>
          <td style="text-align: center;" :class="getRowClass(adr.status)">{{ formatDate(adr.date) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No ADR data available.</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    headerRow: {
      type: Boolean,
      default: false,
    },
    links: {
      type: Boolean,
      default: true,
    },
    maxItems: {
      type: Number,
      default: 10,
    },
    startingItem: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      adrData: [],
    };
  },
  computed: {
    displayAdrData() {
      const startIndex = this.startingItem;
      const endIndex = this.startingItem + this.maxItems;
      return this.adrData.slice(startIndex, endIndex);
    },
  },
  mounted() {
    this.loadAdrData();
  },
  methods: {
    async loadAdrData() {
      try {
        const response = await axios.get('/dist/assets/adr-data.json');
        this.adrData = response.data;
      } catch (error) {
        console.error('Error loading ADR data:', error);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        weekday: 'short', // "Mon"
        year: 'numeric', // "2025"
        month: 'short', // "Apr"
        day: 'numeric', // "6"
      });
    },
    getRowClass(status) {
      switch (status) {
        case 'enforced':
          return 'enforced-row';
        case 'under-review':
          return 'under-review-row';
        case 'deprecated':
          return 'deprecated-row';
        default:
          return '';
      }
    },
  },
};
</script>

<style scoped>
.enforced-row {
  background-color: var(--slidev-theme-secondary);
}
.deprecated-row {
  background-color: var(--slidev-theme-error);
}
.under-review-row {
  background-color: var(--slidev-theme-warn);
}
.enforced-row,
.under-review-row,
.deprecated-row {
  mix-blend-mode: hard-light;
}
</style>
