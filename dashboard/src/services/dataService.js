import { DataEntity } from '../core/entities.js';

export class DataService {
  static getLosRiosData() {
    const years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024];
    const total = [155.0, 158.3, 161.7, 164.3, 165.2, 167.9, 170.7, 174.0, 176.5, 179.4, 165.5, 170.9, 180.1, 175.6, 183.3];
    const male = [89.2, 91.1, 92.8, 94.2, 93.7, 95.1, 96.5, 98.1, 99.4, 100.8, 94.2, 96.8, 101.2, 98.2, 104.8];
    const female = [65.8, 67.2, 68.9, 70.1, 71.5, 72.8, 74.2, 75.9, 77.1, 78.6, 71.3, 74.1, 78.9, 77.4, 78.5];
    
    return new DataEntity(years, total, male, female);
  }
}
