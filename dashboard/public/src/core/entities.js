export class DataEntity {
  constructor(years, total, male, female) {
    this.years = years;
    this.total = total;
    this.male = male;
    this.female = female;
  }

  validate() {
    return this.years.length === this.total.length &&
           this.years.length === this.male.length &&
           this.years.length === this.female.length;
  }
}
