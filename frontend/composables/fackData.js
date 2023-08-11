// const useFakeData = () => {
//     const durationItems = () => {
//         let items = [
//             {
//                 text: "10m",
//                 value: 10,
//             },
//             {
//                 text: "20m",
//                 value: 20,
//             },
//             {
//                 text: "30m",
//                 value: 30,
//             },
//             {
//                 text: "40m",
//                 value: 40,
//             },
//             {
//                 text: "50m",
//                 value: 50,
//             },
//             {
//                 text: "1h",
//                 value: 60,
//             },
//             {
//                 text: "1.5h",
//                 value: 90,
//             },
//             {
//                 text: "2h",
//                 value: 120,
//             },
//             {
//                 text: "2.5h",
//                 value: 150,
//             },
//         ];
//         if (process.browser) {
//             const newItems = JSON.parse(localStorage.getItem('durationItems'))
//             if (newItems.length > 0) {
//                 items = newItems
//             }
//         }

//         return items;
//     }

//     return {
//         durationItems,
//     }
// }

// export default useFakeData





export const durationItems = [
    {
        text: "10m",
        value: 10,
    },
    {
        text: "20m",
        value: 20,
    },
    {
        text: "30m",
        value: 30,
    },
    {
        text: "40m",
        value: 40,
    },
    {
        text: "50m",
        value: 50,
    },
    {
        text: "1h",
        value: 60,
    },
    {
        text: "1.5h",
        value: 90,
    },
    {
        text: "2h",
        value: 120,
    },
    {
        text: "2.5h",
        value: 150,
    },
];

export const toothItems = [
    {
        text: "1",
        value: "1",
    },
    {
        text: "2",
        value: "2",
    },
    {
        text: "3",
        value: "3",
    },
    {
        text: "4",
        value: "4",
    },
    {
        text: "5",
        value: "5",
    },
]
export const treatmentItems = [
    {
        text: "Treatment One",
        value: "1",
    },
    {
        text: "Treatment Two",
        value: "2",
    },
    {
        text: "Treatment Three",
        value: "3",
    },
    {
        text: "Treatment Four",
        value: "4",
    },
    {
        text: "Treatment Five",
        value: "5",
    },
]
export const diagnosticItems = [
    {
        text: "Diagnostic One",
        value: "1",
    },
    {
        text: "Diagnostic Two",
        value: "2",
    },
    {
        text: "Diagnostic Three",
        value: "3",
    },
    {
        text: "Diagnostic Four",
        value: "4",
    },
    {
        text: "Diagnostic Five",
        value: "5",
    },
]
export const clinicItems = [
    {
        id: 1,
        clinicName: "Clinic UCP (owner)",
        startDate: "2022-05-09 09:36:30",
        isOwner: true,
    },
    {
        id: 2,
        clinicName: "Clinic Rainbow ",
        startDate: "2022-08-02 11:25:05",
        isOwner: false,
    },

]