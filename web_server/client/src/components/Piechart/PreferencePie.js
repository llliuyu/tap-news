import React, { Component } from 'react';
import Auth from '../../common/Auth';

import { PieChart, Pie, Legend, Cell, Tooltip, ResponsiveContainer, Sector,
  Label, LabelList } from 'recharts';
import { scaleOrdinal, schemeCategory10 } from 'd3-scale';
import { changeNumberOfData } from './utils';
import _ from 'lodash';

import './PreferencePie.css';
const colors = scaleOrdinal(schemeCategory10).range();

const renderLabelContent = (props) => {
  const { value, percent, x, y, midAngle } = props;

  return (
    <g transform={`translate(${x}, ${y})`} textAnchor={ (midAngle < -90 || midAngle >= 90) ? 'end' : 'start'}>

      <text x={0} y={20}>{`(Percent: ${(percent * 100).toFixed(2)}%)`}</text>
    </g>
  );
};

const renderActiveShape = (props) => {
  const RADIAN = Math.PI / 180;
  const { cx, cy, midAngle, innerRadius, outerRadius, startAngle, endAngle,
    fill, payload, percent } = props;
  const sin = Math.sin(-RADIAN * midAngle);
  const cos = Math.cos(-RADIAN * midAngle);
  const sx = cx + (outerRadius + 10) * cos;
  const sy = cy + (outerRadius + 10) * sin;
  const mx = cx + (outerRadius + 30) * cos;
  const my = cy + (outerRadius + 30) * sin;
  const ex = mx + (cos >= 0 ? 1 : -1) * 22;
  const ey = my;
  const textAnchor = cos >= 0 ? 'start' : 'end';

  return (
    <g>
      <text x={cx} y={cy} dy={8} textAnchor="middle" fill={fill}>{payload.name}</text>
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius}
        outerRadius={outerRadius}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
      />
      <Sector
        cx={cx}
        cy={cy}
        startAngle={startAngle}
        endAngle={endAngle}
        innerRadius={outerRadius + 6}
        outerRadius={outerRadius + 10}
        fill={fill}
      />
      <path d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`} stroke={fill} fill="none"/>
      <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none"/>
      <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} textAnchor={textAnchor} fill="#333">
        {`Count ${payload.value}`}
      </text>
      <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} dy={18} textAnchor={textAnchor} fill="#999">
        {`(percent: ${(percent * 100).toFixed(2)}%)`}
      </text>
    </g>
  );
};

export default class PreferencePie extends Component {
  constructor(props) {
    super(props);
    this.state = {preference: [],
                  activeIndex: 0};
  }

  componentDidMount() {
    this.loadPreference();
  }

  static displayName = 'PieChartDemo';

  onPieEnter = (data, index, e) => {
    this.setState({
      activeIndex: index,
    });
  };

  handleChangeData = () => {
    this.setState(() => _.mapValues(this.state.preference, changeNumberOfData));
  };

  handlePieChartEnter = (a, b, c) => {
    console.log(a, b, c);
  };

  loadPreference() {
    let url = 'http://18.221.159.116:3000/preference/userId/' + Auth.getEmail()

    let request = new Request(encodeURI(url), {
      method: 'GET',
      headers: {
        'Authorization': 'bearer ' + Auth.getToken(),
      },
      cache: false
    });

    fetch(request)
    .then((res) => res.json())
    .then((preference) => {
      if (preference && preference.length !== 0) {
        return this.changeFormat(preference)
      }
    });
  }

  changeFormat(preference) {
    let newPreference = []
    for(let item of preference) {
      newPreference.push({name: item[0], value: item[1]});
    }
    this.setState({preference: newPreference});
  }

  render () {
    
    return (

              <div className="pie-charts">
                {/*<a
                  href="javascript: void(0);"
                  className="btn update"
                  onClick={this.handleChangeData}
                >
                  change data
                </a>
                <br/>
                <p>Simple PieChart</p>*/}
                <div className="pie-chart-wrapper">
                  <PieChart width={800} height={400}>
                    <Legend />
                    
                    <Pie
                      data={this.state.preference}
                      dataKey="value"
                      cx={600}
                      cy={200}
                      startAngle={180}
                      endAngle={-180}
                      innerRadius={60}
                      outerRadius={80}
                      label={renderLabelContent}
                      paddingAngle={5}
                    >
                      {
                        this.state.preference.map((entry, index) => (
                          <Cell key={`slice-${index}`} fill={colors[index % 10]}/>
                        ))
                      }

                      <Label width={50} position="center">
                        News Preference
                      </Label>
                    </Pie>
                  </PieChart>
                </div>
                <div className="video-container">
                    <iframe src="http://18.221.159.116:5601/app/kibana#/dashboard/AV7aV-P4mPuZ5KCkgXTC?embed=true&_g=(refreshInterval%3A('%24%24hashKey'%3A'object%3A492'%2Cdisplay%3A'5%20seconds'%2Cpause%3A!f%2Csection%3A1%2Cvalue%3A5000)%2Ctime%3A(from%3Anow-30m%2Cmode%3Aquick%2Cto%3Anow))" height="600" width="800"></iframe>
                </div>
              </div>

    );
  }
}
