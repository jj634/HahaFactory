// adapted from: https://pusher.com/tutorials/consume-restful-api-react

import React from 'react'
import { Icon, Popup } from 'semantic-ui-react'
import { Doughnut } from 'react-chartjs-2';

const PiChart = ({ cos_score, jac_score, sc_score, similarity }) => {
    return (
        <Popup position='right center' trigger={<Icon className="info_icon" color='teal' name='question circle' size='large' />} hoverable>
            <Popup.Header>Similarity Score Breakdown</Popup.Header>
            <Popup.Content>
                <Doughnut
                    data={
                        {
                            labels: ['Keywords (%)', 'Categories (%)', 'Funny Factor (%)'],
                            datasets: [
                                {
                                    label: 'breakdown',
                                    backgroundColor: [
                                        '#FDC144',
                                        '#FD6585',
                                        '#3DA3E8'
                                    ],
                                    hoverBackgroundColor: [
                                        '#FEDB93',
                                        '#FEBCCA',
                                        '#3DCEE8'
                                    ],
                                    data: [
                                        Number((Number(cos_score) / Number(similarity) * 100).toFixed(1)),
                                        Number((Number(jac_score) / Number(similarity) * 100).toFixed(1)),
                                        Number((Number(sc_score) / Number(similarity) * 100).toFixed(1))
                                    ]
                                }
                            ]
                        }
                    }
                    options={{
                        legend: {
                            display: true,
                            position: 'right',
                            fontSize: 4
                        }
                    }}
                />
            </Popup.Content>
        </Popup>
    )
};

export default PiChart